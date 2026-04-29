"""HubNOC — routes/auth.py"""
import sqlite3, os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.auth import verificar_senha, criar_token, verificar_token

router = APIRouter()
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'noc.db')

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

class LoginIn(BaseModel):
    login: str
    senha: str

@router.post('/login')
async def login(body: LoginIn, db: sqlite3.Connection = Depends(get_db)):
    user = db.execute(
        "SELECT * FROM noc_usuarios WHERE login=? AND ativo=1", [body.login]
    ).fetchone()
    if not user or not verificar_senha(body.senha, user['senha_hash']):
        raise HTTPException(status_code=401, detail='Login ou senha invalidos')
    token = criar_token(user['id'], user['nivel'], user['nome'])
    return {'token': token, 'nome': user['nome'], 'nivel': user['nivel']}

@router.get('/me')
async def me(authorization: str = None):
    if not authorization:
        raise HTTPException(status_code=401, detail='Token nao fornecido')
    token = authorization.replace('Bearer ', '')
    data = verificar_token(token)
    return {'id': data['sub'], 'nivel': data['nivel'], 'nome': data['nome']}
