"""
HubNOC — Patch para routes/tv.py
Adicionar este endpoint ao arquivo existente app/routes/tv.py

Adicione esta função ao router existente:
"""

# Adicionar ao final de app/routes/tv.py:

PATCH_TV_CLIENTES = '''
@router.get('/clientes')
async def clientes_tv(db: sqlite3.Connection = Depends(get_db)):
    """Dados de clientes IXC para TV NOC — Tela 3"""
    from app.services.ixc_db import ixc_conn
    
    try:
        with ixc_conn() as conn:
            cur = conn.cursor()
            # Ativos normais
            cur.execute("""
                SELECT 
                    SUM(online = 'S') as ativos,
                    SUM(online = 'N') as bloqueados,
                    SUM(online = 'SS') as suspensos,
                    COUNT(*) as total
                FROM radusuarios r
                INNER JOIN cliente_contrato cc ON cc.id = r.id_contrato
                WHERE cc.status = 'A'
            """)
            row = cur.fetchone()
            ativos     = row[0] or 0
            bloqueados = row[1] or 0
            suspensos  = row[2] or 0
            total      = row[3] or 1

        distribuicao = [
            {"label": "Ativos",      "val": ativos,     "cor": "#00e5a0"},
            {"label": "Bloqueados",  "val": bloqueados,  "cor": "#ff4466"},
            {"label": "Suspensos",   "val": suspensos,   "cor": "#ffb830"},
        ]
        return {
            "ativos":        ativos,
            "bloqueados":    bloqueados,
            "suspensos":     suspensos,
            "total":         total,
            "distribuicao":  distribuicao,
        }
    except Exception as e:
        # Fallback se IXC não responder
        return {
            "ativos": 0, "bloqueados": 0, "suspensos": 0,
            "total": 0, "distribuicao": [],
            "erro": str(e)
        }
'''

# Também adicionar ao endpoint /estado existente os dados de chamados_lista e chamados_stats:
PATCH_TV_ESTADO = '''
# No endpoint /estado existente, adicionar ao final do return:

    # Chamados lista (para tela 5 da TV)
    chamados_lista = db.execute("""
        SELECT numero, cliente_nome, descricao, status, prioridade, aberto_em
        FROM noc_chamados
        WHERE status IN ('aberto','em_atendimento')
        ORDER BY 
            CASE prioridade WHEN 'critica' THEN 0 WHEN 'alta' THEN 1 ELSE 2 END,
            aberto_em ASC
        LIMIT 10
    """).fetchall()

    chamados_stats_row = db.execute("""
        SELECT
            SUM(status='aberto') as abertos,
            SUM(status='em_atendimento') as em_atendimento,
            SUM(status IN ('resolvido','fechado') AND date(fechado_em)=date(datetime('now','-3 hours'))) as resolvidos_hoje,
            SUM(prioridade='critica' AND status IN ('aberto','em_atendimento')) as criticos
        FROM noc_chamados
        WHERE status IN ('aberto','em_atendimento')
           OR (status IN ('resolvido','fechado') AND date(fechado_em)=date(datetime(\'now\',\'-3 hours\')))
    """).fetchone()

    # Adicionar ao return existente:
    # 'chamados_lista': [dict(c) for c in chamados_lista],
    # 'chamados_stats': dict(chamados_stats_row) if chamados_stats_row else {},
'''

if __name__ == '__main__':
    print("Este arquivo contém os patches para app/routes/tv.py")
    print("\n=== PATCH 1: Adicionar endpoint /api/tv/clientes ===")
    print(PATCH_TV_CLIENTES)
    print("\n=== PATCH 2: Adicionar dados ao /api/tv/estado ===")
    print(PATCH_TV_ESTADO)
