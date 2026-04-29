"""
HubNOC Cliquedf — create_tables.py
Inicializa banco SQLite e cria admin padrao
"""
import sqlite3, hashlib, os, sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'noc.db')

def brt():
    from datetime import timezone, timedelta
    return datetime.now(timezone.utc) - timedelta(hours=3)

def hash_senha(s):
    return hashlib.sha256(s.encode()).hexdigest()

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS noc_usuarios (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        nome        TEXT NOT NULL,
        login       TEXT UNIQUE NOT NULL,
        senha_hash  TEXT NOT NULL,
        nivel       INTEGER DEFAULT 10,
        ativo       INTEGER DEFAULT 1,
        criado_em   TEXT DEFAULT (datetime('now','-3 hours'))
    );

    CREATE TABLE IF NOT EXISTS noc_sensores (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        prtg_id         INTEGER UNIQUE NOT NULL,
        nome            TEXT,
        device          TEXT,
        group_name      TEXT,
        status          TEXT,
        status_raw      INTEGER,
        ultimo_valor    TEXT,
        down_desde      TEXT,
        sync_em         TEXT DEFAULT (datetime('now','-3 hours'))
    );

    CREATE TABLE IF NOT EXISTS noc_incidentes (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo            TEXT NOT NULL,
        tipo              TEXT,
        impacto           TEXT DEFAULT 'medio',
        descricao         TEXT,
        status            TEXT DEFAULT 'aberto',
        sensor_id         INTEGER,
        clientes_afetados INTEGER DEFAULT 0,
        aberto_por        INTEGER REFERENCES noc_usuarios(id),
        aberto_em         TEXT DEFAULT (datetime('now','-3 hours')),
        resolvido_em      TEXT,
        duracao_min       REAL
    );

    CREATE TABLE IF NOT EXISTS noc_chamados (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        numero          TEXT UNIQUE,
        canal           TEXT DEFAULT 'whatsapp',
        cliente_id      INTEGER,
        cliente_nome    TEXT,
        cliente_login   TEXT,
        descricao       TEXT NOT NULL,
        categoria       TEXT DEFAULT 'outros',
        prioridade      TEXT DEFAULT 'normal',
        status          TEXT DEFAULT 'aberto',
        atribuido_a     INTEGER REFERENCES noc_usuarios(id),
        incidente_id    INTEGER REFERENCES noc_incidentes(id),
        sensor_id       INTEGER,
        solucao         TEXT,
        aberto_por      INTEGER REFERENCES noc_usuarios(id),
        aberto_em       TEXT DEFAULT (datetime('now','-3 hours')),
        atualizado_em   TEXT DEFAULT (datetime('now','-3 hours')),
        fechado_em      TEXT
    );

    CREATE TABLE IF NOT EXISTS noc_incidente_timeline (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        incidente_id    INTEGER REFERENCES noc_incidentes(id),
        usuario_id      INTEGER REFERENCES noc_usuarios(id),
        acao            TEXT,
        descricao       TEXT,
        criado_em       TEXT DEFAULT (datetime('now','-3 hours'))
    );

    CREATE TABLE IF NOT EXISTS noc_alertas_prtg (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        prtg_id         INTEGER,
        sensor_nome     TEXT,
        device          TEXT,
        status_anterior TEXT,
        status_novo     TEXT,
        ocorreu_em      TEXT DEFAULT (datetime('now','-3 hours')),
        notificado      INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS noc_config (
        chave   TEXT PRIMARY KEY,
        valor   TEXT
    );
    """)

    # Admin padrao
    admin_existe = c.execute("SELECT id FROM noc_usuarios WHERE login='admin'").fetchone()
    if not admin_existe:
        c.execute("""
            INSERT INTO noc_usuarios (nome, login, senha_hash, nivel)
            VALUES (?, ?, ?, ?)
        """, ('Administrador', 'admin', hash_senha('@!wt0n123'), 99))
        print("[OK] Admin criado: admin / @!wt0n123")
    else:
        print("[OK] Admin ja existe")

    conn.commit()
    conn.close()
    print(f"[OK] Banco criado: {DB_PATH}")

if __name__ == '__main__':
    create_tables()
