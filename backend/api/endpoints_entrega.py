from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
import os

router = APIRouter()
CAMINHO_CSV = "files/recebimentos.csv"

class LeituraEtiqueta(BaseModel):
    codigo_volume: str
    usuario: str

@router.get("/volumes/{id_produto}")
def listar_volumes_por_produto(id_produto: str):
    if not os.path.exists(CAMINHO_CSV):
        return []
    df = pd.read_csv(CAMINHO_CSV)
    filtrado = df[(df["id_produto"].astype(str) == id_produto) & (df["status"] != "ENTREGUE")]
    return filtrado["codigo_volume"].dropna().tolist()

@router.get("/volumes")
def sugerir_volumes(q: str):
    if not os.path.exists(CAMINHO_CSV):
        return []

    df = pd.read_csv(CAMINHO_CSV)
    encontrados = df[df["codigo_volume"].str.contains(q, case=False, na=False)]
    return encontrados["codigo_volume"].drop_duplicates().tolist()

@router.post("/registrar/{codigo_volume}")
def registrar_entrega_por_codigo(codigo_volume: str):
    if not os.path.exists(CAMINHO_CSV):
        raise HTTPException(status_code=404, detail="Arquivo de recebimentos não encontrado.")

    df = pd.read_csv(CAMINHO_CSV)
    idx = df[df["codigo_volume"] == codigo_volume].index
    if idx.empty:
        raise HTTPException(status_code=404, detail=f"Volume {codigo_volume} não encontrado.")

    i = idx[0]
    if df.at[i, "status"] == "ENTREGUE":
        return {"mensagem": "Este volume já foi entregue anteriormente."}

    df.at[i, "status"] = "ENTREGUE"
    df.at[i, "usuario"] += " (entregue)"
    df.at[i, "data_entrega"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df.to_csv(CAMINHO_CSV, index=False)
    return {"mensagem": f"Volume {codigo_volume} entregue com sucesso."}
