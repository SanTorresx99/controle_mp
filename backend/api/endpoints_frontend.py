# backend/api/endpoints_frontend.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend", "templates"))

@router.get("/recebimento/web", response_class=HTMLResponse)
def exibir_formulario_recebimento(request: Request):
    return templates.TemplateResponse("recebimento.html", {"request": request})

@router.get("/login/web", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/painel/web", response_class=HTMLResponse)
def painel_web(request: Request):
    return templates.TemplateResponse("painel.html", {"request": request})

@router.get("/usuarios/web", response_class=HTMLResponse)
def usuarios_web(request: Request):
    return templates.TemplateResponse("usuarios.html", {"request": request})

@router.get("/entregas/web", response_class=HTMLResponse)
def entregas_web(request: Request):
    return templates.TemplateResponse("entregas.html", {"request": request})

@router.get("/etiqueta/reimpressao/web", response_class=HTMLResponse)
def reimpressao_etiquetas_web(request: Request):
    from glob import glob
    etiquetas = glob("files/etiquetas/*.pdf")  # ou outro caminho onde as etiquetas estão
    etiquetas = [e.replace("\\", "/") for e in etiquetas]
    return templates.TemplateResponse("etiquetas.html", {"request": request, "etiquetas": etiquetas})

@router.get("/validacao/web", response_class=HTMLResponse)
def validacao_web(request: Request):
    return templates.TemplateResponse("validacao.html", {"request": request})
