
@router.get('/mapa')
async def olts_mapa(db: sqlite3.Connection = Depends(get_db)):
    """OLTs com coordenadas para o mapa"""
    try:
        with ixc_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        r.id as olt_id, r.descricao as olt_nome,
                        r.ip, r.fabricante_modelo as modelo, r.uptime,
                        p.pop as pop_nome, p.latitude, p.longitude,
                        COUNT(u.id) as total_clientes,
                        SUM(u.online IN ('S','SS')) as online,
                        SUM(u.online = 'N' AND cc.status = 'A') as offline_problema,
                        SUM(u.online = 'SS') as suspenso
                    FROM radpop_radio r
                    LEFT JOIN radpop p ON p.id = r.id_pop
                    LEFT JOIN radusuarios u ON u.id_transmissor = r.id
                    LEFT JOIN cliente_contrato cc ON cc.id_cliente = u.id_cliente
                    WHERE r.fabricante_modelo IN
                        ('HW','CIAGPON','CIAEPON','ZTEC610','VSOL',
                         'INTELBRASEPON','TH','DC','O')
                      AND p.latitude IS NOT NULL AND p.latitude != ''
                    GROUP BY r.id
                    ORDER BY total_clientes DESC
                """)
                olts = cur.fetchall()

        sensores_prtg = {}
        try:
            rows = db.execute("SELECT nome, device, status, ultimo_valor FROM noc_sensores").fetchall()
            for s in rows:
                sensores_prtg[(s['device'] or '').upper()] = dict(s)
                sensores_prtg[(s['nome'] or '').upper()] = dict(s)
        except: pass

        resultado = []
        for o in olts:
            olt = dict(o)
            olt['online']           = int(olt['online'] or 0)
            olt['offline_problema'] = int(olt['offline_problema'] or 0)
            olt['suspenso']         = int(olt['suspenso'] or 0)
            olt['total_clientes']   = int(olt['total_clientes'] or 0)
            total = olt['total_clientes']
            olt['pct_online'] = round(olt['online'] / total * 100, 1) if total > 0 else 0

            nome_upper = (olt['olt_nome'] or '').upper()
            prtg = None
            for chave, sensor in sensores_prtg.items():
                palavras = [p for p in nome_upper.split() if len(p) > 3]
                if any(p in chave for p in palavras):
                    prtg = sensor; break
            olt['prtg_status']  = prtg['status'] if prtg else 'Desconhecido'
            olt['prtg_trafico'] = prtg['ultimo_valor'] if prtg else '—'
            resultado.append(olt)

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro: {str(e)}')


@router.get('/caixas')
async def caixas_ftth(db: sqlite3.Connection = Depends(get_db)):
    """Caixas FTTH com coordenadas para o mapa"""
    try:
        with ixc_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, descricao, latitude, longitude,
                           capacidade, bairro, status, id_transmissor
                    FROM rad_caixa_ftth
                    WHERE latitude IS NOT NULL AND latitude != ''
                      AND longitude IS NOT NULL AND longitude != ''
                    LIMIT 2000
                """)
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro: {str(e)}')
