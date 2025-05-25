import os
import csv
import pandas as pd
from datetime import datetime

CAMINHO_CSV = "files/recebimentos.csv"
CAMINHO_ENTREGAS = "files/entregas.csv"

def salvar_volumes_csv(volumes: list[dict]):
    """
    Salva os volumes fracionados no arquivo CSV de recebimento.
    Se o arquivo não existir, cria com o cabeçalho.
    """
    os.makedirs(os.path.dirname(CAMINHO_CSV), exist_ok=True)
    arquivo_existe = os.path.exists(CAMINHO_CSV)

    with open(CAMINHO_CSV, mode='a', newline='', encoding='utf-8') as f:
        campos = [
            "numero_nf", "id_produto", "produto", "especie", "subespecie", "unidade",
            "volume_num", "quantidade", "fornecedor", "data_recebimento",
            "usuario", "status", "codigo_volume", "data_entrega"
        ]
        writer = csv.DictWriter(f, fieldnames=campos)
        if not arquivo_existe:
            writer.writeheader()
        for v in volumes:
            if "data_entrega" not in v:
                v["data_entrega"] = ""
            writer.writerow(v)

def buscar_codigos_volume_por_produto(id_produto: str):
    if not os.path.exists(CAMINHO_CSV):
        return []
    df = pd.read_csv(CAMINHO_CSV)
    filtrado = df[(df["id_produto"].astype(str) == str(id_produto)) & (df["status"] != "ENTREGUE")]
    return filtrado["codigo_volume"].dropna().unique().tolist()


def atualizar_status_entrega(codigo_volume: str):
    """
    Atualiza o status de um volume para ENTREGUE no CSV.
    """
    if not os.path.exists(CAMINHO_CSV):
        raise FileNotFoundError("Arquivo CSV de recebimentos não encontrado.")

    df = pd.read_csv(CAMINHO_CSV)

    if codigo_volume not in df["codigo_volume"].values:
        raise ValueError("Código do volume não encontrado.")

    linha = df[df["codigo_volume"] == codigo_volume]
    if linha.iloc[0]["status"] == "ENTREGUE":
        raise ValueError("Este volume já foi entregue.")

    df.loc[df["codigo_volume"] == codigo_volume, "status"] = "ENTREGUE"
    df.loc[df["codigo_volume"] == codigo_volume, "data_entrega"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df.to_csv(CAMINHO_CSV, index=False)
    return f"Entrega registrada com sucesso para {codigo_volume}."

def registrar_entrega_csv(info: dict):
    os.makedirs(os.path.dirname(CAMINHO_ENTREGAS), exist_ok=True)
    arquivo_existe = os.path.exists(CAMINHO_ENTREGAS)

    with open(CAMINHO_ENTREGAS, mode='a', newline='', encoding='utf-8') as f:
        campos = [
            "codigo_volume", "produto", "quantidade", "id_produto",
            "usuario", "data_entrega"
        ]
        writer = csv.DictWriter(f, fieldnames=campos)
        if not arquivo_existe:
            writer.writeheader()
        writer.writerow(info)