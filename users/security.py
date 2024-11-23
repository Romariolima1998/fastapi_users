from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from http import HTTPStatus

from fastapi import status
from pwdlib import PasswordHash
from jwt import encode, decode, InvalidTokenError
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from cachetools import TTLCache

from users.settings import Settings
from users.database.database import get_session
from users.database.models import User

oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')
pwdhash = PasswordHash.recommended()

list_revoked_tokens = TTLCache(maxsize=10000, ttl=Settings().TOKEN_EXPIRE)

def revoked_token(token: str):
    if token in list(list_revoked_tokens.keys()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"})
    try:
        payload =decode(token, Settings().SECRET_KEY, algorithms=Settings().ALGORITHM)
        list_revoked_tokens[token] = "revoked"

    
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )



def hash(password:str) -> str:
    return pwdhash.hash(password)

def verify(password: str, password_hash: str) -> bool:
    return pwdhash.verify(password, password_hash)



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta( minutes=Settings().TOKEN_EXPIRE)

    to_encode.update({"exp": expire})

    encoded_jwt = encode(to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM)

    return encoded_jwt


async def get_current_user( session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_schema)):
    if token in list(list_revoked_tokens.keys()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    credential_exceptions = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode(token, Settings().SECRET_KEY, algorithms=Settings().ALGORITHM)

        username = payload.get('sub')

        if not username:
            raise credential_exceptions
        
    except ExpiredSignatureError as error:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(error),
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    except PyJWTError:
        raise credential_exceptions
    
    try:
        user = await session.scalar(
            select(User).where(User.username == username)
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(error),
            headers={'WWW-Authenticate': 'Bearer'})
    
    return user

