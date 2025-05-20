#backend/logic/validacao_firebird.py
from fastapi import APIRouter
import pandas as pd
from backend.database.firebird_conn import conectar

router = APIRouter()

def carregar_df_produtos():
    conn = conectar()
    sql = """
        SELECT
            p.id_produto,
            p.nome AS nome_produto,
            e.nome AS especie,
            s.nome AS subespecie,
            um.sigla as unidade
        FROM produto p
        LEFT JOIN especie e ON e.id_especie = p.id_especie
        LEFT JOIN sub_especie s on s.id_sub_especie = p.id_sub_especie
        left join unidade_medida um on um.id_unidade_medida = p.id_unidade_medida
        WHERE p.ativo = 1
    """
    df = pd.read_sql(sql, conn)
    conn.close()
    df.columns = df.columns.str.lower()
    return df
