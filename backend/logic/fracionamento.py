# backend/logic/fracionamento.py

from backend.logic.validacao_firebird import carregar_df_produtos

def buscar_info_produto(id_produto: int):
    """
    Retorna as informações de nome, espécie, subespécie e unidade do produto.
    Adiciona tratamento para erros de DataFrame vazio ou coluna ausente.
    """
    df_produtos = carregar_df_produtos()

    if df_produtos.empty or "id_produto" not in df_produtos.columns:
        raise ValueError("Erro: DataFrame de produtos vazio ou sem a coluna 'id_produto'.")

    linha = df_produtos[df_produtos["id_produto"] == id_produto]
    if linha.empty:
        raise ValueError(f"Produto com ID {id_produto} não encontrado no ERP.")

    return linha.to_dict(orient="records")[0]


def gerar_volumes(dados):
    """
    Gera a lista de volumes fracionados a partir do total informado.
    Se 'quantidades_personalizadas' for informada, usa os valores manuais.
    Caso contrário, fraciona automaticamente em partes iguais.
    """
    info = buscar_info_produto(dados.id_produto)
    volumes = []

    if dados.quantidades_personalizadas:
        if len(dados.quantidades_personalizadas) != dados.quantidade_volumes:
            raise ValueError("Número de volumes informado difere da lista de quantidades.")

        soma_personalizada = round(sum(dados.quantidades_personalizadas), 2)
        if soma_personalizada != round(dados.quantidade_total, 2):
            raise ValueError(f"Soma das quantidades ({soma_personalizada}) difere do total informado ({dados.quantidade_total}).")

        qtd_por_volume_lista = dados.quantidades_personalizadas
    else:
        qtd_auto = round(dados.quantidade_total / dados.quantidade_volumes, 2)
        qtd_por_volume_lista = [qtd_auto] * (dados.quantidade_volumes - 1)
        ultima = round(dados.quantidade_total - sum(qtd_por_volume_lista), 2)
        qtd_por_volume_lista.append(ultima)

    for i, qtd in enumerate(qtd_por_volume_lista, start=1):
        volumes.append({
            "numero_nf": dados.numero_nf,
            "id_produto": dados.id_produto,
            "produto": info["nome_produto"],
            "especie": info["especie"],
            "subespecie": info["subespecie"],
            "unidade": info["unidade"],
            "volume_num": i,
            "quantidade": qtd,
            "fornecedor": dados.fornecedor,
            "data_recebimento": dados.data_recebimento.isoformat(),
            "usuario": dados.usuario,
            "status": "AGUARDANDO_FISCAL",
            "codigo_volume": f"MP-{dados.numero_nf}-{dados.id_produto}-{i}"
        })

    return volumes
