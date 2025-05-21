# backend/logic/usuarios.py

import os
import json
import bcrypt
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()

USUARIOS_PATH = os.path.join("files", "usuarios.json")
SECRET_KEY = os.getenv("SECRET_KEY")

def carregar_usuarios():
    if not os.path.exists(USUARIOS_PATH):
        return []
    with open(USUARIOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_usuario(usuario: str, senha: str):
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    token = gerar_token(usuario)
    usuarios = carregar_usuarios()
    usuarios.append({"usuario": usuario, "senha_hash": senha_hash, "token": token})
    with open(USUARIOS_PATH, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)
    return token

def validar_login(usuario: str, senha: str) -> str | None:
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario and bcrypt.checkpw(senha.encode(), u["senha_hash"].encode()):
            return u.get("token")
    return None

def gerar_token(usuario: str) -> str:
    payload = {
        "sub": usuario,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verificar_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Exemplo de uso direto (teste local)
if __name__ == "__main__":
    print("Adicionando admin teste...")
    token = salvar_usuario("admin", "1234")
    print("Token criado:", token)
    print("Login admin/1234:", validar_login("admin", "1234"))
    print("Login admin/errado:", validar_login("admin", "errado"))
