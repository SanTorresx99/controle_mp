#backend/api/endpoints_recebimento.py
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from typing import Optional, List

from backend.logic.fracionamento import gerar_volumes
from backend.logic.csv_handler import salvar_volumes_csv
from backend.logic.etiquetas import (gerar_etiqueta, gerar_etiquetas_em_lote)


router = APIRouter()

class PreCadastro(BaseModel):
    numero_nf: int
    fornecedor: str
    data_recebimento: date
    id_produto: int
    quantidade_total: float
    quantidade_volumes: int
    usuario: str
    quantidades_personalizadas: Optional[List[float]] = None  # NOVO

@router.post("/novo")
def receber_pre_cadastro(dados: PreCadastro):
    try:
        # limpar_etiquetas_antigas()  # Descomente se a função estiver implementada
        volumes = gerar_volumes(dados)
        salvar_volumes_csv(volumes)
        etiquetas_geradas = []
        caminho_pdf = gerar_etiquetas_em_lote(volumes)
        etiquetas_geradas.append(caminho_pdf)

        return {
            "mensagem": f"{len(volumes)} volumes gerados com sucesso.",
            "codigo_base": f"MP-{dados.numero_nf}-{dados.id_produto}",
            "volumes": volumes,
            "etiquetas_pdf": etiquetas_geradas
        }
    except Exception as e:
        return {"erro": str(e)}
