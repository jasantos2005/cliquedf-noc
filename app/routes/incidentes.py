"""HubNOC — routes/incidentes.py"""
import sqlite3
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.main import get_db

router = APIRouter()

def brt():
    return (datetime.now(timezone.utc) - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')

class IncidenteIn(BaseModel):
    titulo: str
    tipo: str = 'equipamento'
    impacto: str = 'medio'
    descricao: Optional[str] = None
    sensor_id: Optional[int] = None
    clientes_afetados: int = 0
    aberto_por: Optional[int] = None

class TimelineIn(BaseModel):
    usuario_id: Optional[int] = None
    acao: str = 'atualizacao'
    descricao: str

@router.get('')
async def listar_incidentes(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("""
        SELECT i.*, u.nome as aberto_por_nome
        FROM noc_incidentes i
        LEFT JOIN noc_usuarios u ON u.id = i.aberto_por
        ORDER BY i.aberto_em DESC
    """).fetchall()
    return [dict(r) for r in rows]

@router.get('/ativos')
async def incidentes_ativos(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("""
        SELECT i.*, u.nome as aberto_por_nome
        FROM noc_incidentes i
        LEFT JOIN noc_usuarios u ON u.id = i.aberto_por
        WHERE i.status != 'resolvido'
        ORDER BY i.aberto_em DESC
    """).fetchall()
    return [dict(r) for r in rows]

@router.post('')
async def abrir_incidente(body: IncidenteIn, db: sqlite3.Connection = Depends(get_db)):
    db.execute("""
        INSERT INTO noc_incidentes
            (titulo, tipo, impacto, descricao, sensor_id, clientes_afetados, aberto_por, aberto_em)
        VALUES (?,?,?,?,?,?,?,?)
    """, [body.titulo, body.tipo, body.impacto, body.descricao,
          body.sensor_id, body.clientes_afetados, body.aberto_por, brt()])
    db.commit()
    inc_id = db.execute("SELECT last_insert_rowid() as id").fetchone()['id']
    # Timeline: abertura
    db.execute("""
        INSERT INTO noc_incidente_timeline (incidente_id, usuario_id, acao, descricao)
        VALUES (?,?,?,?)
    """, [inc_id, body.aberto_por, 'abertura', body.descricao or 'Incidente aberto'])
    db.commit()
    return dict(db.execute("SELECT * FROM noc_incidentes WHERE id=?", [inc_id]).fetchone())

@router.put('/{inc_id}')
async def atualizar_incidente(
    inc_id: int, body: dict,
    db: sqlite3.Connection = Depends(get_db)
):
    inc = db.execute("SELECT * FROM noc_incidentes WHERE id=?", [inc_id]).fetchone()
    if not inc:
        raise HTTPException(status_code=404, detail='Incidente nao encontrado')

    novo_status = body.get('status')
    if novo_status == 'resolvido':
        # Calcular duracao
        abertura = datetime.strptime(inc['aberto_em'], '%Y-%m-%d %H:%M:%S')
        agora = datetime.now(timezone.utc) - timedelta(hours=3)
        agora = agora.replace(tzinfo=None)
        duracao = round((agora - abertura).total_seconds() / 60, 1)
        db.execute("""
            UPDATE noc_incidentes
            SET status='resolvido', resolvido_em=?, duracao_min=?
            WHERE id=?
        """, [brt(), duracao, inc_id])
    else:
        campos = []
        vals = []
        for k in ('titulo', 'impacto', 'descricao', 'status', 'clientes_afetados'):
            if k in body:
                campos.append(f"{k}=?"); vals.append(body[k])
        if campos:
            vals.append(inc_id)
            db.execute(f"UPDATE noc_incidentes SET {', '.join(campos)} WHERE id=?", vals)
    db.commit()
    return dict(db.execute("SELECT * FROM noc_incidentes WHERE id=?", [inc_id]).fetchone())

@router.post('/{inc_id}/timeline')
async def add_timeline(
    inc_id: int, body: TimelineIn,
    db: sqlite3.Connection = Depends(get_db)
):
    db.execute("""
        INSERT INTO noc_incidente_timeline (incidente_id, usuario_id, acao, descricao, criado_em)
        VALUES (?,?,?,?,?)
    """, [inc_id, body.usuario_id, body.acao, body.descricao, brt()])
    db.commit()
    return {'ok': True}

@router.get('/{inc_id}/timeline')
async def get_timeline(inc_id: int, db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("""
        SELECT t.*, u.nome as usuario_nome
        FROM noc_incidente_timeline t
        LEFT JOIN noc_usuarios u ON u.id = t.usuario_id
        WHERE t.incidente_id=?
        ORDER BY t.criado_em ASC
    """, [inc_id]).fetchall()
    return [dict(r) for r in rows]
