#backend/api/endpoints_etiqueta.py
from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import pandas as pd
from backend.logic.etiquetas import gerar_etiqueta

router = APIRouter()

templates = Jinja2Templates(directory="frontend/templates")
ETIQUETA_DIR = "files/etiquetas"
CSV_RECEBIMENTOS = "files/recebimentos.csv"

@router.get("/{codigo_volume}")
def baixar_etiqueta(codigo_volume: str):
    """
    Baixa a etiqueta PDF já gerada, se existir.
    """
    caminho = os.path.join(ETIQUETA_DIR, f"{codigo_volume}.pdf")
    if not os.path.exists(caminho):
        return {"erro": f"Etiqueta '{codigo_volume}' não encontrada."}

    return FileResponse(path=caminho, filename=f"{codigo_volume}.pdf", media_type='application/pdf')

@router.get("/gerar/{codigo_volume}")
def regenerar_etiqueta(codigo_volume: str):
    """
    Regenera a etiqueta PDF a partir dos dados do CSV.
    """
    if not os.path.exists(CSV_RECEBIMENTOS):
        return {"erro": "Arquivo de recebimentos não encontrado."}

    df = pd.read_csv(CSV_RECEBIMENTOS)
    linha = df[df["codigo_volume"] == codigo_volume]
    if linha.empty:
        return {"erro": f"Volume {codigo_volume} não encontrado no CSV."}

    volume = linha.to_dict(orient="records")[0]
    caminho_pdf = gerar_etiqueta(volume)
    return FileResponse(path=caminho_pdf, filename=f"{codigo_volume}.pdf", media_type='application/pdf')

@router.get("/etiquetas/web", response_class=HTMLResponse)
def exibir_etiquetas(request: Request):
    arquivos = sorted([
        os.path.join(ETIQUETA_DIR, nome)
        for nome in os.listdir(ETIQUETA_DIR)
        if nome.endswith(".pdf")
    ])
    return templates.TemplateResponse("etiquetas.html", {"request": request, "etiquetas": arquivos})
