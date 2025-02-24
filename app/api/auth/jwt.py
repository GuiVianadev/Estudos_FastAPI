from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from services.user_service import UserService
from core.security import create_access_token, create_refresh_token
from schemas.auth_schema import tokenSchema
from schemas.user_schema import UserDetail
from models.user_model import User
from api.dependecies.user_deps import get_current_user
from pydantic import ValidationError 
from core.config import settings
from schemas.auth_schema import TokenPayload
from jose import jwt

auth_router = APIRouter()

@auth_router.post('/login', summary='Cria Acess Token e Refresh Token', response_model=tokenSchema)
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Any:
    usuario = await UserService.authenticate(
        email = data.username,
        password= data.password
    )
    if not usuario:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email ou senha estão incorretos'
        )
    # Criar access_token
    return {
        "access_token" : create_access_token(usuario.user_id),
        "refresh_token" : create_refresh_token(usuario.user_id)
    }


@auth_router.post('/test-token', summary= 'Testando o token', response_model=UserDetail)
async def test_token(user : User = Depends(get_current_user)):
    return user

@auth_router.post('/refresh', summary='Refresh', response_model=tokenSchema)
async def refresh_token(refresh_token : str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            details='Token inválido',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    user = await UserService.get_user_by_id(token_data.sub)

    if not User:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            details = 'Não foi possível encontrar o usuário',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    return {
        "access_token" : create_access_token(user.user_id),
        "refresh_token" : create_refresh_token(user.user_id)
    }