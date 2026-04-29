"""HubNOC — routes/admin.py"""
import sqlite3, hashlib
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.main import get_db

router = APIRouter()

def hash_senha(s): return hashlib.sha256(s.encode()).hexdigest()

class UsuarioIn(BaseModel):
    nome: str
    login: str
    senha: str
    nivel: int = 10

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    senha: Optional[str] = None
    nivel: Optional[int] = None
    ativo: Optional[int] = None

@router.get('/usuarios')
async def listar_usuarios(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute(
        "SELECT id, nome, login, nivel, ativo, criado_em FROM noc_usuarios ORDER BY nivel DESC, nome"
    ).fetchall()
    return [dict(r) for r in rows]

@router.post('/usuarios')
async def criar_usuario(body: UsuarioIn, db: sqlite3.Connection = Depends(get_db)):
    existe = db.execute("SELECT id FROM noc_usuarios WHERE login=?", [body.login]).fetchone()
    if existe:
        raise HTTPException(status_code=400, detail='Login ja existe')
    db.execute("""
        INSERT INTO noc_usuarios (nome, login, senha_hash, nivel)
        VALUES (?,?,?,?)
    """, [body.nome, body.login, hash_senha(body.senha), body.nivel])
    db.commit()
    return {'ok': True, 'login': body.login}

@router.put('/usuarios/{uid}')
async def atualizar_usuario(uid: int, body: UsuarioUpdate, db: sqlite3.Connection = Depends(get_db)):
    campos, vals = [], []
    if body.nome:    campos.append("nome=?");        vals.append(body.nome)
    if body.senha:   campos.append("senha_hash=?");  vals.append(hash_senha(body.senha))
    if body.nivel is not None: campos.append("nivel=?"); vals.append(body.nivel)
    if body.ativo is not None: campos.append("ativo=?"); vals.append(body.ativo)
    if not campos:
        raise HTTPException(status_code=400, detail='Nada para atualizar')
    vals.append(uid)
    db.execute(f"UPDATE noc_usuarios SET {', '.join(campos)} WHERE id=?", vals)
    db.commit()
    return {'ok': True}
