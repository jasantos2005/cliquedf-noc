"""
HubNOC — ixc_db.py
Conexao MySQL IXC (somente SELECT)
"""
import pymysql, os
from dotenv import load_dotenv

load_dotenv()

def ixc_conn():
    return pymysql.connect(
        host=os.getenv('IXC_HOST', '186.148.228.42'),
        port=int(os.getenv('IXC_PORT', 3306)),
        user=os.getenv('IXC_USER', 'escrita'),
        password=os.getenv('IXC_PASS', 'CZ5QYpdjc1RqAP'),
        database=os.getenv('IXC_DB', 'ixcprovedor'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10
    )

def ixc_select(sql, params=None):
    with ixc_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or [])
            return cur.fetchall()

def ixc_select_one(sql, params=None):
    with ixc_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or [])
            return cur.fetchone()

def buscar_cliente(termo):
    """Busca cliente por nome, CPF/CNPJ ou login PPPoE"""
    with ixc_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT
                    c.id, c.razao, c.cnpj_cpf,
                    r.login as login_pppoe,
                    cc.status as contrato_status
                FROM cliente c
                LEFT JOIN radusuarios r ON r.id_cliente = c.id
                LEFT JOIN cliente_contrato cc ON cc.id_cliente = c.id
                WHERE c.razao LIKE %s
                   OR c.cnpj_cpf LIKE %s
                   OR r.login LIKE %s
                LIMIT 10
            """, [f'%{termo}%', f'%{termo}%', f'%{termo}%'])
            return cur.fetchall()

def historico_cliente(cliente_id, limite=20):
    """Retorna ultimas OS do cliente no IXC"""
    with ixc_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    o.id,
                    a.assunto,
                    o.status,
                    CONVERT_TZ(o.data_abertura, '+00:00', '-03:00') as data_abertura,
                    CONVERT_TZ(o.data_fechamento, '+00:00', '-03:00') as data_fechamento,
                    o.solucao
                FROM su_oss_chamado o
                LEFT JOIN su_oss_assunto a ON a.id = o.id_assunto
                WHERE o.id_cliente = %s
                ORDER BY o.data_abertura DESC
                LIMIT %s
            """, [cliente_id, limite])
            return cur.fetchall()
