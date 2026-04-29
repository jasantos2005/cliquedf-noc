"""
HubNOC — services/auth.py
JWT SHA256
"""
import hashlib, os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status

SECRET = os.getenv('SECRET_KEY', 'hubnoc_dev_key_2024')
ALGO   = 'HS256'

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    return hash_senha(senha) == hash_armazenado

def criar_token(user_id: int, nivel: int, nome: str) -> str:
    payload = {
        'sub': str(user_id),
        'nivel': nivel,
        'nome': nome,
        'exp': datetime.now(timezone.utc) + timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def verificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalido ou expirado'
        )

def requer_nivel(token_data: dict, nivel_minimo: int):
    if token_data.get('nivel', 0) < nivel_minimo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Acesso negado'
        )
