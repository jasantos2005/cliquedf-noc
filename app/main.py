"""
HubNOC Cliquedf — main.py
FastAPI + rotas HTML + API
"""
import sqlite3, os
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title='HubNOC Cliquedf', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'],
                   allow_methods=['*'], allow_headers=['*'])

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'noc.db')

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# ── Registrar rotas ──────────────────────────────────────────
from app.routes import auth, olts, chamados, sensores, clientes, incidentes, dashboard, tv, admin
app.include_router(olts.router,       prefix='/api/olts')
app.include_router(auth.router,       prefix='/api/auth')
app.include_router(chamados.router,   prefix='/api/chamados')
app.include_router(sensores.router,   prefix='/api/sensores')
app.include_router(clientes.router,   prefix='/api/clientes')
app.include_router(incidentes.router, prefix='/api/incidentes')
app.include_router(dashboard.router,  prefix='/api/dashboard')
app.include_router(tv.router,         prefix='/api/tv')
app.include_router(admin.router,      prefix='/api/admin')

app.mount('/static', StaticFiles(directory=os.path.join(os.path.dirname(__file__), '..', 'static')), name='static')

STATIC = os.path.join(os.path.dirname(__file__), '..', 'static')

def html(nome):
    with open(os.path.join(STATIC, nome)) as f:
        return HTMLResponse(f.read())

@app.get('/',          response_class=HTMLResponse)
async def root():       return html('login.html')

@app.get('/login',     response_class=HTMLResponse)
async def login_page(): return html('login.html')

@app.get('/dashboard', response_class=HTMLResponse)
async def dashboard_page(): return html('dashboard.html')

@app.get('/chamados',  response_class=HTMLResponse)
async def chamados_page(): return html('chamados.html')

@app.get('/incidentes', response_class=HTMLResponse)
async def incidentes_page(): return html('incidentes.html')

@app.get('/sensores',  response_class=HTMLResponse)
async def sensores_page(): return html('sensores.html')

@app.get('/cliente',   response_class=HTMLResponse)
async def cliente_page(): return html('cliente.html')

@app.get('/tv',        response_class=HTMLResponse)
async def tv_page():    return html('tv.html')

@app.get('/admin',     response_class=HTMLResponse)
async def admin_page(): return html('admin.html')

@app.get('/health')
async def health():
    return {'status': 'ok', 'sistema': 'HubNOC Cliquedf', 'versao': '1.0.0'}

@app.get('/olts', response_class=HTMLResponse)
async def olts_page(): return html('olts.html')

@app.get('/mapa', response_class=HTMLResponse)
async def mapa_page(): return html('mapa.html')
