from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
import os

router = APIRouter()

CAMINHO_CSV = "files/recebimentos.csv"

class LeituraEtiqueta(BaseModel):
    codigo_volume: str
    usuario: str

@router.post("/registrar")
def registrar_entrega(dados: LeituraEtiqueta):
    if not os.path.exists(CAMINHO_CSV):
        return {"erro": "Arquivo de recebimentos não encontrado."}

    df = pd.read_csv(CAMINHO_CSV)

    idx = df[df["codigo_volume"] == dados.codigo_volume].index
    if idx.empty:
        return {"erro": f"Volume {dados.codigo_volume} não encontrado."}

    i = idx[0]
    if df.at[i, "status"] == "ENTREGUE":
        return {"mensagem": "Este volume já foi entregue anteriormente."}

    df.at[i, "status"] = "ENTREGUE"
    df.at[i, "usuario"] = dados.usuario + " (entregue)"
    df.at[i, "data_entrega"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df.to_csv(CAMINHO_CSV, index=False)
    return {"mensagem": f"Volume {dados.codigo_volume} entregue com sucesso."}

@router.get("/status/{codigo_volume}")
def consultar_status_volume(codigo_volume: str):
    if not os.path.exists(CAMINHO_CSV):
        return {"erro": "Arquivo de recebimentos não encontrado."}

    try:
        df = pd.read_csv(CAMINHO_CSV)
    except pd.errors.EmptyDataError:
        return {"erro": "Arquivo de recebimentos está vazio ou corrompido."}

    linha = df[df["codigo_volume"] == codigo_volume]
    if linha.empty:
        return {"erro": f"Volume {codigo_volume} não encontrado."}

    info = linha.to_dict(orient="records")[0]
    return {
        "codigo_volume": info["codigo_volume"],
        "produto": info["produto"],
        "quantidade": info["quantidade"],
        "status": info["status"],
        "data_recebimento": info["data_recebimento"],
        "usuario": info["usuario"],
        "entregue_em": info.get("data_entrega", None)
    }
