from fastapi import APIRouter, HTTPException, status, Depends
import pymongo.errors
from schemas.user_schema import UserAuth, UserDetail
from services.user_service import UserService
import pymongo
from models.user_model import User
from api.dependecies.user_deps import get_current_user

user_router = APIRouter()

@user_router.post('/adiciona', summary='Adiciona Usuário', response_model=UserDetail)
async def adiciona_usuario(data:UserAuth):
    try:
        return await UserService.create_user(data)
    except  pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username ou email deste usuario já existe"
        )
    

@user_router.get('/me', summary='Detalhes do Usuário logado', response_model=UserDetail)
async def get_me(user: User = Depends(get_current_user)):
    return user