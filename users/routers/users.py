from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from users.database.database import get_session
from users.database.models import User
from users.schemas import (UserCreateInput, UserCreateOutput,
                           UserUpdateInput, MessageOutput,
                           PasswordRecoveryInput)
from users.security import hash
from users.security import get_current_user
from users.utils import validate_email, validate_password


router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]



@router.post('/create',status_code=status.HTTP_201_CREATED, response_model=UserCreateOutput)
async def user_create(dados: UserCreateInput, session: Session):

    try:
        user_username = await session.scalar(
            select(User).where(User.username == dados.username)
        )
        if user_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='username alredy exists' )

    
        user_email = await session.scalar(
                select(User).where(User.email == dados.email)
            )
        if user_email:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='email alredy exists'
                )
    

        if not validate_email(dados.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='email invalid'
            )

        if not validate_password(dados.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='very weak password, must have at least 8 digits, a special character and an uppercase letter'
            )

        user = User(dados.username, hash(dados.password), dados.email)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
    
    except SQLAlchemyError as error:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(error))
    

@router.get('/list')
async def user_list(session: Session, offset: int = 0, limit: int = 10) -> list[UserCreateOutput]:
    try:
        users = await session.scalars(
            select(User).offset(offset).limit(limit)
        )

        return users.all()
    
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(error))
    

@router.put('/update/{id}', response_model=UserCreateOutput)
async def user_update(id: int, dados:UserUpdateInput, session: Session, current_user: CurrentUser):

    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='permission denid'
        )
    
    if dados.username:
        try:
            user = await session.scalar(
                select(User).where(User.username == dados.username)
            )
            print (user)
            if user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='username alredy exists'
                )
        except SQLAlchemyError as error:
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(error))
    
    if dados.email:
        try:
            user = await session.scalar(
                select(User).where(User.email == dados.email)
            )
            if user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='email alredy exists'
                )
        except SQLAlchemyError as error:
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(error))
    
    if dados.username:
        current_user.username = dados.username

    if dados.email:
        if not validate_email(dados.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='email invalid')
        
        current_user.email = dados.email

    if dados.password:
        if not validate_password(dados.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='very weak password, must have at least 8 digits, a special character and an uppercase letter'
            )
        
        current_user.password = hash(dados.password)

    await session.commit()
    await session.refresh(current_user)

    return current_user

@router.delete('/delete/{id}')
async def user_delete(id: int, current_user: CurrentUser, session: Session) -> MessageOutput:

    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='permission denid'
        )
    
    await session.delete(current_user)
    await session.commit()

    return {'message': 'user deleted'}

