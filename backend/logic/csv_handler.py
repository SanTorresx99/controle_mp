import os
import csv

CAMINHO_CSV = "files/recebimentos.csv"

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
            "usuario", "status", "codigo_volume"
        ]
        writer = csv.DictWriter(f, fieldnames=campos)
        if not arquivo_existe:
            writer.writeheader()
        for v in volumes:
            writer.writerow(v)
