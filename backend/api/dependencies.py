# backend/api/dependencies.py

from fastapi import Request, HTTPException
from backend.logic.usuarios import verificar_token

def verificar_autenticacao(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token ausente")

    token = token.replace("Bearer ", "")
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    return payload["sub"]  # retorna o nome do usuário autenticado
