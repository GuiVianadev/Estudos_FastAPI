from passlib.context import CryptContext
from typing import Union, Any
from datetime import datetime, timedelta, timezone
from jose import jwt
from core.config import settings 


password_context = CryptContext (
    schemes=["bcrypt"],
    deprecated = "auto"
)

def get_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password:str, hashed_password:str) -> bool:
    return password_context.verify(password, hashed_password)

def create_access_token(subject: Union[str, Any], expires_delta:int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta =  datetime.now(timezone.utc) + timedelta(
            minutes= settings.ACCES_TOKEN_EXPIRE_MINUTES
        )

    info_jwt = {
        "exp": expires_delta,
        "sub": str(subject)
    }

    jwt_encoded = jwt.encode(
        info_jwt,
        settings.JWT_SECRET_KEY,
        algorithm= settings.ALGORITHM
    )
    return jwt_encoded

def create_refresh_token(subject: Union[str, Any], expires_delta:int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta =  datetime.now(timezone.utc) + timedelta(
            minutes= settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    info_jwt = {
        "exp": expires_delta,
        "sub": str(subject)
    }

    jwt_encoded = jwt.encode(
        info_jwt,
        settings.JWT_REFRESH_SECRET_KEY,
    )
    return jwt_encoded