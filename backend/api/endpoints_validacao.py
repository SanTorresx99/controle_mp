from fastapi import APIRouter, Query
from backend.database.firebird_conn import conectar
import pandas as pd

router = APIRouter()

@router.get("/produtos")
def listar_produtos(q: str = Query(..., min_length=2)):
    """
    Retorna lista de produtos cujo nome ou ID contenha o texto 'q'.
    """
    try:
        conn = conectar()
        sql = f"""
            SELECT FIRST 20
                p.id_produto,
                p.nome AS nome_produto,
                e.nome AS especie,
                se.nome AS subespecie,
                um.sigla AS unidade
            FROM produto p
            LEFT JOIN especie e ON e.id_especie = p.id_especie
            LEFT JOIN sub_especie se ON se.id_sub_especie = p.id_sub_especie
            LEFT JOIN unidade_medida um ON um.id_unidade_medida = p.id_unidade_medida
            WHERE UPPER(p.nome) LIKE '%{q.upper()}%'
            OR CAST(p.id_produto AS VARCHAR(20)) LIKE '%{q}%'
            ORDER BY p.nome
        """
        df = pd.read_sql(sql, conn)
        conn.close()
        return df.to_dict(orient="records")
    except Exception as e:
        return {"erro": str(e)}

@router.get("/fornecedores")
def listar_fornecedores(q: str = Query(..., min_length=2)):
    """
    Retorna lista de fornecedores cujo nome contenha o texto 'q'.
    """
    try:
        conn = conectar()
        sql = f"""
            SELECT FIRST 20
                p.nome,
                p.nome_fantasia
            FROM fornecedor f
            INNER JOIN pessoa p ON p.id_pessoa = f.id_pessoa
            WHERE UPPER(p.nome) LIKE '%{q.upper()}%'
            OR UPPER(p.nome_fantasia) LIKE '%{q.upper()}%'
            ORDER BY p.nome
        """
        df = pd.read_sql(sql, conn)
        conn.close()
        return df.to_dict(orient="records")
    except Exception as e:
        return {"erro": str(e)}
