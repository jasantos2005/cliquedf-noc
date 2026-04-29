"""HubNOC — routes/dashboard.py"""
import sqlite3
from fastapi import APIRouter, Depends
from app.main import get_db

router = APIRouter()

@router.get('/resumo')
async def resumo(db: sqlite3.Connection = Depends(get_db)):
    sensores = db.execute("""
        SELECT
            COUNT(*) as total,
            SUM(status='OK') as ok,
            SUM(status='DOWN') as down,
            SUM(status='Aviso') as aviso,
            SUM(status='Incomum') as incomum,
            SUM(status='Pausado') as pausado
        FROM noc_sensores
    """).fetchone()

    chamados = db.execute("""
        SELECT
            COUNT(*) as total,
            SUM(status='aberto') as abertos,
            SUM(status='em_atendimento') as em_atendimento,
            SUM(status IN ('resolvido','fechado')) as resolvidos_hoje
        FROM noc_chamados
        WHERE date(aberto_em) = date(datetime('now','-3 hours'))
    """).fetchone()

    incidentes = db.execute("""
        SELECT COUNT(*) as ativos
        FROM noc_incidentes
        WHERE status != 'resolvido'
    """).fetchone()

    alertas_recentes = db.execute("""
        SELECT * FROM noc_alertas_prtg
        ORDER BY ocorreu_em DESC LIMIT 10
    """).fetchall()

    down_list = db.execute("""
        SELECT nome, device, down_desde
        FROM noc_sensores WHERE status='DOWN'
        ORDER BY down_desde ASC
    """).fetchall()

    return {
        'sensores': dict(sensores),
        'chamados': dict(chamados),
        'incidentes_ativos': incidentes['ativos'],
        'alertas_recentes': [dict(a) for a in alertas_recentes],
        'sensores_down': [dict(d) for d in down_list]
    }
