# backend/api/endpoints_usuarios.py
from fastapi import APIRouter, HTTPException, Depends
from backend.logic.usuarios import carregar_usuarios, salvar_usuarios, salvar_usuario
from backend.api.dependencies import somente_master

router = APIRouter()

@router.get("/listar", dependencies=[Depends(somente_master)])
def listar_usuarios():
    usuarios = carregar_usuarios()
    return [{"usuario": u["usuario"], "nivel": u.get("nivel", "usuario")} for u in usuarios]

@router.post("/criar", dependencies=[Depends(somente_master)])
def criar_usuario(dados: dict):
    try:
        usuario = dados.get("usuario")
        senha = dados.get("senha")
        nivel = dados.get("nivel")

        if not all([usuario, senha, nivel]):
            raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios.")

        salvar_usuario(usuario, senha, nivel)
        return {"mensagem": f"Usuário '{usuario}' criado com sucesso."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao criar usuário.")

@router.delete("/excluir/{usuario}", dependencies=[Depends(somente_master)])
def excluir_usuario(usuario: str):
    usuarios = carregar_usuarios()

    if usuario == "admin" or usuario == "master":
        raise HTTPException(status_code=403, detail="Não é permitido excluir o usuário master.")

    novos = [u for u in usuarios if u["usuario"] != usuario]
    if len(novos) == len(usuarios):
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    salvar_usuarios(novos)
    return {"mensagem": f"Usuário '{usuario}' excluído com sucesso."}
