from fastapi import FastAPI
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.user_model import User
from models.todo_model import Todo
from api.api_v1.router import router
from contextlib import asynccontextmanager

# Definindo o gerenciador de contexto lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código para execução na inicialização
    cliente_db = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).todoapp
    await init_beanie(
        database=cliente_db,
        document_models=[User, Todo]
    )
    yield
    # Código para execução no desligamento (se necessário)
    # Aqui você pode adicionar lógica para quando a aplicação estiver sendo encerrada

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan  # Passando o gerenciador de contexto lifespan
)

app.include_router(
    router, 
    prefix=settings.API_V1_STR
)
