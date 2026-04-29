"""HubNOC — routes/chamados.py"""
import sqlite3
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.main import get_db

router = APIRouter()

def brt():
    return (datetime.now(timezone.utc) - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')

def gerar_numero(db):
    from datetime import datetime
    mes = (datetime.now(timezone.utc) - timedelta(hours=3)).strftime('%Y%m')
    total = db.execute(
        "SELECT COUNT(*) as n FROM noc_chamados WHERE numero LIKE ?", [f'NOC-{mes}-%']
    ).fetchone()['n']
    return f"NOC-{mes}-{str(total+1).zfill(4)}"

class ChamadoIn(BaseModel):
    canal: str = 'whatsapp'
    cliente_id: Optional[int] = None
    cliente_nome: Optional[str] = None
    cliente_login: Optional[str] = None
    descricao: str
    categoria: str = 'outros'
    prioridade: str = 'normal'
    atribuido_a: Optional[int] = None
    incidente_id: Optional[int] = None
    sensor_id: Optional[int] = None
    aberto_por: Optional[int] = None

class ChamadoUpdate(BaseModel):
    status: Optional[str] = None
    atribuido_a: Optional[int] = None
    incidente_id: Optional[int] = None
    solucao: Optional[str] = None
    prioridade: Optional[str] = None
    categoria: Optional[str] = None

@router.get('')
async def listar_chamados(
    status: Optional[str] = Query(None),
    categoria: Optional[str] = Query(None),
    atribuido_a: Optional[int] = Query(None),
    db: sqlite3.Connection = Depends(get_db)
):
    sql = """
        SELECT c.*,
               u.nome as atendente_nome
        FROM noc_chamados c
        LEFT JOIN noc_usuarios u ON u.id = c.atribuido_a
        WHERE 1=1
    """
    params = []
    if status:
        sql += " AND c.status=?"; params.append(status)
    if categoria:
        sql += " AND c.categoria=?"; params.append(categoria)
    if atribuido_a:
        sql += " AND c.atribuido_a=?"; params.append(atribuido_a)
    sql += " ORDER BY c.aberto_em DESC LIMIT 200"
    rows = db.execute(sql, params).fetchall()
    return [dict(r) for r in rows]

@router.post('')
async def abrir_chamado(body: ChamadoIn, db: sqlite3.Connection = Depends(get_db)):
    numero = gerar_numero(db)
    db.execute("""
        INSERT INTO noc_chamados
            (numero, canal, cliente_id, cliente_nome, cliente_login,
             descricao, categoria, prioridade, atribuido_a, incidente_id,
             sensor_id, aberto_por, aberto_em, atualizado_em)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, [numero, body.canal, body.cliente_id, body.cliente_nome, body.cliente_login,
          body.descricao, body.categoria, body.prioridade, body.atribuido_a,
          body.incidente_id, body.sensor_id, body.aberto_por, brt(), brt()])
    db.commit()
    chamado = db.execute("SELECT * FROM noc_chamados WHERE numero=?", [numero]).fetchone()
    return dict(chamado)

@router.get('/{chamado_id}')
async def detalhe_chamado(chamado_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("""
        SELECT c.*, u.nome as atendente_nome
        FROM noc_chamados c
        LEFT JOIN noc_usuarios u ON u.id = c.atribuido_a
        WHERE c.id=?
    """, [chamado_id]).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail='Chamado nao encontrado')
    return dict(row)

@router.put('/{chamado_id}')
async def atualizar_chamado(
    chamado_id: int, body: ChamadoUpdate,
    db: sqlite3.Connection = Depends(get_db)
):
    chamado = db.execute("SELECT * FROM noc_chamados WHERE id=?", [chamado_id]).fetchone()
    if not chamado:
        raise HTTPException(status_code=404, detail='Chamado nao encontrado')

    updates = []
    params = []
    if body.status is not None:
        updates.append("status=?"); params.append(body.status)
        if body.status in ('resolvido', 'fechado'):
            updates.append("fechado_em=?"); params.append(brt())
    if body.atribuido_a is not None:
        updates.append("atribuido_a=?"); params.append(body.atribuido_a)
        if chamado['status'] == 'aberto':
            updates.append("status='em_atendimento'")
    if body.incidente_id is not None:
        updates.append("incidente_id=?"); params.append(body.incidente_id)
    if body.solucao is not None:
        updates.append("solucao=?"); params.append(body.solucao)
    if body.prioridade is not None:
        updates.append("prioridade=?"); params.append(body.prioridade)
    if body.categoria is not None:
        updates.append("categoria=?"); params.append(body.categoria)

    updates.append("atualizado_em=?"); params.append(brt())
    params.append(chamado_id)

    db.execute(f"UPDATE noc_chamados SET {', '.join(updates)} WHERE id=?", params)
    db.commit()
    return dict(db.execute("SELECT * FROM noc_chamados WHERE id=?", [chamado_id]).fetchone())
