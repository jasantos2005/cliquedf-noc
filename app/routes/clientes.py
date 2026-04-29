"""HubNOC — routes/clientes.py"""
from fastapi import APIRouter, Query, HTTPException
from app.services.ixc_db import buscar_cliente, historico_cliente

router = APIRouter()

@router.get('/buscar')
async def buscar(q: str = Query(..., min_length=2)):
    try:
        resultado = buscar_cliente(q)
        return resultado or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro IXC: {str(e)}')

@router.get('/{cliente_id}/historico')
async def historico(cliente_id: int, limite: int = 20):
    try:
        return historico_cliente(cliente_id, limite)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro IXC: {str(e)}')
