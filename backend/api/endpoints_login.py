# backend/api/endpoints_login.py

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from backend.logic.usuarios import validar_login

router = APIRouter()

@router.post("/login")
def login(usuario: str = Form(...), senha: str = Form(...)):
    token = validar_login(usuario, senha)
    if token:
        return {"token": token}
    return JSONResponse(status_code=401, content={"erro": "Usuário ou senha inválidos."})
