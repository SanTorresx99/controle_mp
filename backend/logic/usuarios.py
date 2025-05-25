# backend/logic/usuarios.py
import json
import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

USUARIOS_JSON = "files/usuarios.json"
SECRET_KEY = os.getenv("SECRET_KEY")


def carregar_usuarios():
    if not os.path.exists(USUARIOS_JSON):
        return []
    with open(USUARIOS_JSON, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def salvar_usuarios(lista):
    with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)


def gerar_token(usuario, nivel="usuario"):
    payload = {
        "sub": usuario,
        "nivel": nivel,
        "exp": datetime.utcnow() + timedelta(days=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def salvar_usuario(usuario, senha, nivel="usuario"):
    usuarios = carregar_usuarios()
    if any(u["usuario"] == usuario for u in usuarios):
        raise ValueError("Usuário já existe")

    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    token = gerar_token(usuario, nivel)

    usuarios.append({
        "usuario": usuario,
        "senha_hash": senha_hash,
        "nivel": nivel,
        "token": token
    })
    salvar_usuarios(usuarios)


def validar_login(usuario, senha):
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario and bcrypt.checkpw(senha.encode(), u["senha_hash"].encode()):
            return gerar_token(usuario, u.get("nivel", "usuario"))
    return None
