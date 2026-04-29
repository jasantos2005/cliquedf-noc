"""HubNOC — routes/olts.py"""
import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from app.main import get_db
from app.services.ixc_db import ixc_conn

router = APIRouter()

def _olts_ixc():
    with ixc_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    r.id as olt_id,
                    r.descricao as olt_nome,
                    r.ip,
                    r.fabricante_modelo as modelo,
                    r.uptime,
                    r.id_pop,
                    p.pop as pop_nome,
                    COUNT(u.id) as total_clientes,
                    SUM(u.online IN ('S','SS')) as online,
                    SUM(u.online = 'N' AND cc.status = 'A') as offline_problema,
                    SUM(u.online = 'N' AND cc.status != 'A') as offline_cancelado,
                    SUM(u.online = 'SS') as suspenso
                FROM radpop_radio r
                LEFT JOIN radpop p ON p.id = r.id_pop
                LEFT JOIN radusuarios u ON u.id_transmissor = r.id
                LEFT JOIN cliente_contrato cc ON cc.id_cliente = u.id_cliente
                WHERE r.fabricante_modelo IN
                    ('HW','CIAGPON','CIAEPON','ZTEC610','VSOL',
                     'INTELBRASEPON','TH','DC','O')
                GROUP BY r.id
                ORDER BY total_clientes DESC
            """)
            return cur.fetchall()

def _clientes_olt(olt_id, limite=500):
    with ixc_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    u.id, u.login, u.online, u.ip,
                    c.razao as cliente_nome, c.cnpj_cpf,
                    cc.status as contrato_status,
                    f.sinal_rx, f.sinal_tx, f.status_potencia,
                    f.causa_ultima_queda, f.ponno, f.slotno, f.onu_numero
                FROM radusuarios u
                LEFT JOIN cliente c ON c.id = u.id_cliente
                LEFT JOIN cliente_contrato cc ON cc.id_cliente = c.id
                LEFT JOIN radpop_radio_cliente_fibra f ON f.id_login = u.id
                WHERE u.id_transmissor = %s
                ORDER BY
                    CASE u.online WHEN 'N' THEN 0 WHEN 'SS' THEN 1 ELSE 2 END,
                    c.razao ASC
                LIMIT %s
            """, [olt_id, limite])
            return cur.fetchall()

def _portas_olt(olt_id):
    with ixc_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, numero_pon, descricao,
                       quantidade_onus, quantidade_onus_autorizadas, potencia_pon
                FROM radpop_radio_porta
                WHERE id_pop_radio = %s ORDER BY numero_pon ASC
            """, [olt_id])
            return cur.fetchall()

def _sinal_onus_olt(olt_id):
    with ixc_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT f.status_potencia, COUNT(*) as qtd,
                       AVG(f.sinal_rx) as sinal_medio,
                       MIN(f.sinal_rx) as sinal_min,
                       MAX(f.sinal_rx) as sinal_max
                FROM radpop_radio_cliente_fibra f
                WHERE f.id_transmissor = %s
                  AND f.sinal_rx IS NOT NULL AND f.sinal_rx != 0
                GROUP BY f.status_potencia
            """, [olt_id])
            return cur.fetchall()

def _classificar_cliente(online, contrato):
    if online in ('S',) and contrato == 'A': return 'online'
    if online in ('S',) and contrato == 'I': return 'online_inativo'
    if online == 'SS': return 'suspenso'
    if online == 'N' and contrato == 'A':  return 'offline_problema'
    if online == 'N' and contrato == 'I':  return 'cancelado'
    return 'outros'

@router.get('')
async def listar_olts(db: sqlite3.Connection = Depends(get_db)):
    try:
        olts_ixc = _olts_ixc()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro IXC: {str(e)}')

    sensores_prtg = {}
    try:
        rows = db.execute("SELECT nome, device, status, ultimo_valor FROM noc_sensores").fetchall()
        for s in rows:
            sensores_prtg[(s['device'] or '').upper()] = dict(s)
            sensores_prtg[(s['nome'] or '').upper()] = dict(s)
    except: pass

    resultado = []
    for o in olts_ixc:
        olt = dict(o)
        olt['online']           = int(olt['online'] or 0)
        olt['offline_problema'] = int(olt['offline_problema'] or 0)
        olt['offline_cancelado']= int(olt['offline_cancelado'] or 0)
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
                        (SELECT COUNT(*) FROM radusuarios u2 WHERE u2.id_transmissor = r.id) as total_clientes,
                        (SELECT COUNT(*) FROM radusuarios u2 WHERE u2.id_transmissor = r.id AND u2.online IN ('S','SS')) as online,
                        (SELECT COUNT(*) FROM radusuarios u2
                         LEFT JOIN cliente_contrato cc2 ON cc2.id_cliente = u2.id_cliente
                         WHERE u2.id_transmissor = r.id AND u2.online = 'N' AND cc2.status = 'A') as offline_problema,
                        (SELECT COUNT(*) FROM radusuarios u2 WHERE u2.id_transmissor = r.id AND u2.online = 'SS') as suspenso
                    FROM radpop_radio r
                    LEFT JOIN radpop p ON p.id = r.id_pop
                    WHERE r.fabricante_modelo IN
                        ('HW','CIAGPON','CIAEPON','ZTEC610','VSOL',
                         'INTELBRASEPON','TH','DC','O')
                      AND p.latitude IS NOT NULL AND p.latitude != ''
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
@router.get('/{olt_id}')
async def detalhe_olt(olt_id: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        with ixc_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT r.id as olt_id, r.descricao as olt_nome,
                           r.ip, r.fabricante_modelo as modelo, r.uptime,
                           p.pop as pop_nome
                    FROM radpop_radio r
                    LEFT JOIN radpop p ON p.id = r.id_pop
                    WHERE r.id = %s
                """, [olt_id])
                olt = cur.fetchone()
        if not olt:
            raise HTTPException(status_code=404, detail='OLT não encontrada')

        clientes    = _clientes_olt(olt_id, 500)
        portas      = _portas_olt(olt_id)
        sinal_stats = _sinal_onus_olt(olt_id)

        clientes_lista = []
        contadores = {'online':0,'online_inativo':0,'suspenso':0,'offline_problema':0,'cancelado':0,'outros':0}
        for c in clientes:
            classe = _classificar_cliente(c['online'], c['contrato_status'])
            contadores[classe] = contadores.get(classe, 0) + 1
            clientes_lista.append({
                'id': c['id'], 'login': c['login'],
                'cliente_nome': c['cliente_nome'],
                'online': c['online'] in ('S','SS'),
                'online_raw': c['online'],
                'contrato_status': c['contrato_status'],
                'classe': classe,
                'ip': c['ip'],
                'sinal_rx': float(c['sinal_rx']) if c['sinal_rx'] else None,
                'sinal_tx': float(c['sinal_tx']) if c['sinal_tx'] else None,
                'status_potencia': c['status_potencia'],
                'causa_ultima_queda': c['causa_ultima_queda'],
                'ponno': c['ponno'], 'slotno': c['slotno'], 'onu_numero': c['onu_numero'],
            })

        total = len(clientes_lista)
        sinal_resumo = [{'status': s['status_potencia'] or 'indefinido',
            'qtd': int(s['qtd']),
            'sinal_medio': round(float(s['sinal_medio'] or 0), 2),
            'sinal_min': round(float(s['sinal_min'] or 0), 2),
            'sinal_max': round(float(s['sinal_max'] or 0), 2)} for s in sinal_stats]

        portas_lista = [{'id': p['id'], 'numero_pon': p['numero_pon'],
            'descricao': p['descricao'], 'quantidade_onus': p['quantidade_onus'],
            'quantidade_onus_autorizadas': p['quantidade_onus_autorizadas'],
            'potencia_pon': float(p['potencia_pon']) if p['potencia_pon'] else None} for p in portas]

        sensor_prtg = None
        nome_upper = (olt['olt_nome'] or '').upper()
        rows = db.execute("SELECT * FROM noc_sensores").fetchall()
        for s in rows:
            palavras = [p for p in nome_upper.split() if len(p) > 3]
            if any(p in (s['device'] or '').upper() for p in palavras):
                sensor_prtg = dict(s); break

        return {
            'olt': dict(olt),
            'resumo': {
                'total': total,
                'online': contadores['online'],
                'online_inativo': contadores['online_inativo'],
                'suspenso': contadores['suspenso'],
                'offline_problema': contadores['offline_problema'],
                'cancelado': contadores['cancelado'],
                'pct_online': round(contadores['online']/total*100, 1) if total > 0 else 0
            },
            'clientes': clientes_lista,
            'portas': portas_lista,
            'sinal_stats': sinal_resumo,
            'sensor_prtg': sensor_prtg,
        }
    except HTTPException: raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro: {str(e)}')

@router.get('/{olt_id}/grafico')
async def grafico_olt(olt_id: int, horas: int = 6, db: sqlite3.Connection = Depends(get_db)):
    """Retorna histórico de tráfego PRTG para gráfico"""
    # Buscar sensor PRTG correspondente à OLT
    with ixc_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT descricao FROM radpop_radio WHERE id=%s", [olt_id])
            olt = cur.fetchone()
    if not olt:
        raise HTTPException(status_code=404, detail='OLT não encontrada')

    # Encontrar sensor PRTG pelo nome
    sensores = db.execute("SELECT * FROM noc_sensores").fetchall()
    sensor_id = None
    nome_upper = (olt['descricao'] or '').upper()
    palavras = [p for p in nome_upper.split() if len(p) > 3]
    for s in sensores:
        if any(p in (s['nome'] or '').upper() for p in palavras):
            sensor_id = s['prtg_id']; break
        if any(p in (s['device'] or '').upper() for p in palavras):
            sensor_id = s['prtg_id']; break

    if not sensor_id:
        raise HTTPException(status_code=404, detail='Sensor PRTG não encontrado para esta OLT')

    try:
        from app.services.prtg_service import get_historico_sensor
        hist = get_historico_sensor(sensor_id, horas=horas)
        dados = hist.get('histdata', [])

        # Processar dados
        pontos = []
        for d in dados:
            val_raw = d.get('value_raw', 0) or 0
            mbps = round(val_raw / 1_000_000, 2)  # bytes/s → Mbit/s
            pontos.append({
                'hora': d['datetime'][11:16],  # HH:MM
                'datetime': d['datetime'],
                'mbps': mbps,
                'label': d.get('value', '—')
            })

        # Calcular estatísticas
        valores = [p['mbps'] for p in pontos if p['mbps'] > 0]
        stats = {
            'atual': pontos[-1]['mbps'] if pontos else 0,
            'pico':  round(max(valores), 2) if valores else 0,
            'media': round(sum(valores)/len(valores), 2) if valores else 0,
            'minimo': round(min(valores), 2) if valores else 0,
            'sensor_id': sensor_id,
            'horas': horas,
        }

        return {'pontos': pontos, 'stats': stats}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro PRTG: {str(e)}')

