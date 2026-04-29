"""
HubNOC — cron_sync_prtg.py
Sync sensores PRTG → SQLite a cada 2min
Detecta mudancas de status e registra alertas
"""
import sqlite3, os, sys
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.prtg_service import get_sensores, mapear_status

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'noc.db')

def brt():
    return (datetime.now(timezone.utc) - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')

def sync():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        sensores = get_sensores()
    except Exception as e:
        print(f"[ERRO] PRTG inacessivel: {e}")
        conn.close()
        return

    atualizados = 0
    alertas = 0

    for s in sensores:
        prtg_id    = s.get('objid')
        nome       = s.get('name', '')
        device     = s.get('device', '')
        group_name = s.get('group', '')
        status_raw = s.get('status_raw', 0)
        status     = mapear_status(status_raw)
        ultimo_val = s.get('lastvalue', '')

        # Busca estado anterior
        anterior = c.execute(
            "SELECT status, down_desde FROM noc_sensores WHERE prtg_id=?", [prtg_id]
        ).fetchone()

        down_desde = None
        if anterior:
            status_ant = anterior['status']

            # Detecta mudanca de status
            if status_ant != status:
                c.execute("""
                    INSERT INTO noc_alertas_prtg
                        (prtg_id, sensor_nome, device, status_anterior, status_novo, ocorreu_em)
                    VALUES (?,?,?,?,?,?)
                """, [prtg_id, nome, device, status_ant, status, brt()])
                alertas += 1

            # Mantem down_desde se continua DOWN
            if status == 'DOWN':
                down_desde = anterior['down_desde'] or brt()
        else:
            if status == 'DOWN':
                down_desde = brt()

        # Upsert sensor
        c.execute("""
            INSERT INTO noc_sensores
                (prtg_id, nome, device, group_name, status, status_raw, ultimo_valor, down_desde, sync_em)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(prtg_id) DO UPDATE SET
                nome=excluded.nome,
                device=excluded.device,
                group_name=excluded.group_name,
                status=excluded.status,
                status_raw=excluded.status_raw,
                ultimo_valor=excluded.ultimo_valor,
                down_desde=excluded.down_desde,
                sync_em=excluded.sync_em
        """, [prtg_id, nome, device, group_name, status, status_raw, ultimo_val, down_desde, brt()])
        atualizados += 1

    conn.commit()
    conn.close()
    print(f"[{brt()}] PRTG sync: {atualizados} sensores | {alertas} mudancas de status")

if __name__ == '__main__':
    sync()
