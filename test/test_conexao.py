from backend.database.firebird_conn import conectar

def testar_conexao():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PRODUTO")
        resultado = cursor.fetchone()
        print(f"[✅] Conexão bem-sucedida! Data atual do banco: {resultado[0]}")
        conn.close()
    except Exception as e:
        print(f"[❌] Erro ao conectar ao Firebird: {e}")

if __name__ == "__main__":
    testar_conexao()
