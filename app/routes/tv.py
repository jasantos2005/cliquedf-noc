"""HubNOC — routes/tv.py"""
import sqlite3
from fastapi import APIRouter, Depends
from app.main import get_db

router = APIRouter()

@router.get('/estado')
async def estado_tv(db: sqlite3.Connection = Depends(get_db)):
    """Dados para TV NOC — sem auth, apenas leitura"""
    sensores = db.execute("""
        SELECT COUNT(*) as total,
               SUM(status='OK') as ok,
               SUM(status='DOWN') as down,
               SUM(status='Aviso') as aviso,
               SUM(status='Incomum') as incomum
        FROM noc_sensores
    """).fetchone()

    down_list = db.execute("""
        SELECT nome, device, group_name, down_desde
        FROM noc_sensores WHERE status='DOWN'
        ORDER BY down_desde ASC
    """).fetchall()

    olts = db.execute("""
        SELECT nome, device, status, status_raw, ultimo_valor, down_desde
        FROM noc_sensores
        WHERE UPPER(nome) LIKE '%OLT%' OR UPPER(device) LIKE '%OLT%'
        ORDER BY status_raw ASC
    """).fetchall()

    chamados_abertos = db.execute("""
        SELECT COUNT(*) as n FROM noc_chamados
        WHERE status IN ('aberto','em_atendimento')
    """).fetchone()

    incidentes_ativos = db.execute("""
        SELECT id, titulo, impacto, tipo, aberto_em
        FROM noc_incidentes WHERE status != 'resolvido'
        ORDER BY aberto_em DESC
    """).fetchall()

    alertas = db.execute("""
        SELECT sensor_nome, device, status_anterior, status_novo, ocorreu_em
        FROM noc_alertas_prtg
        ORDER BY ocorreu_em DESC LIMIT 20
    """).fetchall()

    return {
        'sensores': dict(sensores),
        'down_list': [dict(d) for d in down_list],
        'olts': [dict(o) for o in olts],
        'chamados_abertos': chamados_abertos['n'],
        'incidentes_ativos': [dict(i) for i in incidentes_ativos],
        'alertas_recentes': [dict(a) for a in alertas]
    }
