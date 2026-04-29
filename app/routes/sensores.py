"""HubNOC — routes/sensores.py"""
import sqlite3
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.main import get_db

router = APIRouter()

@router.get('/resumo')
async def resumo_sensores(db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("""
        SELECT
            COUNT(*) as total,
            SUM(status='OK') as ok,
            SUM(status='DOWN') as down,
            SUM(status='Aviso') as aviso,
            SUM(status='Pausado') as pausado,
            SUM(status='Incomum') as incomum
        FROM noc_sensores
    """).fetchone()
    return dict(row)

@router.get('/down')
async def sensores_down(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("""
        SELECT * FROM noc_sensores
        WHERE status='DOWN'
        ORDER BY down_desde ASC
    """).fetchall()
    return [dict(r) for r in rows]

@router.get('/olts')
async def sensores_olts(db: sqlite3.Connection = Depends(get_db)):
    """Retorna sensores relacionados a OLTs"""
    rows = db.execute("""
        SELECT * FROM noc_sensores
        WHERE UPPER(nome) LIKE '%OLT%'
           OR UPPER(device) LIKE '%OLT%'
        ORDER BY status ASC, device ASC
    """).fetchall()
    return [dict(r) for r in rows]

@router.get('/alertas')
async def alertas_recentes(limite: int = 50, db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("""
        SELECT * FROM noc_alertas_prtg
        ORDER BY ocorreu_em DESC
        LIMIT ?
    """, [limite]).fetchall()
    return [dict(r) for r in rows]

@router.get('')
async def listar_sensores(
    status: Optional[str] = Query(None),
    busca: Optional[str] = Query(None),
    db: sqlite3.Connection = Depends(get_db)
):
    sql = "SELECT * FROM noc_sensores WHERE 1=1"
    params = []
    if status:
        sql += " AND status=?"; params.append(status)
    if busca:
        sql += " AND (nome LIKE ? OR device LIKE ?)";
        params += [f'%{busca}%', f'%{busca}%']
    sql += " ORDER BY status_raw ASC, device ASC"
    rows = db.execute(sql, params).fetchall()
    return [dict(r) for r in rows]
