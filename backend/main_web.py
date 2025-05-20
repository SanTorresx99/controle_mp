from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import (
    endpoints_recebimento,
    endpoints_validacao,
    endpoints_entrega,
    endpoints_etiqueta,
    endpoints_frontend
)
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Controle de Matéria-Prima",
    description="API para pré-cadastro, validação e entrega de volumes de matéria-prima com fracionamento e leitura de código de barras.",
    version="1.0.0"
)

# Middleware para permitir testes via navegador e integração com frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restringir!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas
app.include_router(endpoints_recebimento.router, prefix="/recebimento", tags=["Pré-Cadastro"])
app.include_router(endpoints_validacao.router, prefix="/validacao", tags=["Validação"])
app.include_router(endpoints_entrega.router, prefix="/entrega", tags=["Entrega"])
app.include_router(endpoints_etiqueta.router, prefix="/etiqueta", tags=["Etiquetas"])
app.include_router(endpoints_frontend.router, tags=["Frontend"])
#app.include_router(endpoints_etiqueta.router)
app.mount("/files", StaticFiles(directory="files"), name="files")