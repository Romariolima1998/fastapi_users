from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from fastapi_mail import MessageSchema

from users.database.database import get_session
from users.database.models import User
from users.security import create_access_token, get_current_user, revoked_token, verify, oauth2_schema
from users.schemas import TokenOutput, PasswordRecoveryInput, MessageOutput, RevokedTokenInput
from users.utils import email


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=TokenOutput)
async def create_token(dados: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):

    try:
        user = await session.scalar(
            select(User).where(User.username == dados.username)
        )
    
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )
    
    if not user or not verify(dados.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password'
        )
    
    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}

@router.post('/refresh', response_model=TokenOutput)
async def refresh_token(current_user: User = Depends(get_current_user)):
    
    access_token = create_access_token({'sub': current_user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/logout', response_model=MessageOutput)
async def logout(token:str = Depends(oauth2_schema)):
    revoked_token(token)

    return {'message': 'logout token'}


@router.post('/email/password-recovery', response_model=MessageOutput)
async def email_password_recovery(dados: PasswordRecoveryInput, session: AsyncSession = Depends(get_session)):
    user = await session.scalar(
        select(User).where(User.email == dados.email)
    )

    if not user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='email not exists'
        )
    
    access_token = create_access_token(data={'sub': user.username})
    
    message = MessageSchema(
        subject="Recuperação de senha",
        recipients=[user.email],
        body=f"Use o seguinte token para recuperar sua senha: {'Bearer '+ access_token}",
        subtype="plain"
    )
    
    fm = await email()
    await fm.send_message(message)

    return{'message': 'check your email inbox'}