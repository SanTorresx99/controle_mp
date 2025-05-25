#backend/api/dependencies.py

from fastapi import Request, HTTPException, Depends
from backend.logic.usuarios import verificar_token

def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token ausente")

    token = token.replace("Bearer ", "")
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    return payload  # inclui 'sub' e 'nivel'

def somente_master(payload=Depends(get_current_user)):
    if payload["nivel"] != "master":
        raise HTTPException(status_code=403, detail="Acesso restrito ao usuário master")
    return payload

def somente_gestor_ou_mais(payload=Depends(get_current_user)):
    if payload["nivel"] not in ["master", "gestor"]:
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para gestor ou master")
    return payload
