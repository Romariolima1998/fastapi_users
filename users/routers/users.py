from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from users.database.database import get_session
from users.database.models import User
from users.schemas import UserCreateInput, UserCreateOutput
from users.security import hash, verify


router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[AsyncSession, Depends(get_session)]



@router.post('/create',status_code=status.HTTP_201_CREATED, response_model=UserCreateOutput)
async def user_create(dados: UserCreateInput, session: Session):

    user = User(dados.username, hash(dados.password), dados.email)

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
    
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='error saving to database')
    

@router.get('/list')
async def user_list(session: Session, offset: int = 0, limit: int = 10) -> list[UserCreateOutput]:
    users = await session.scalars(
        select(User).offset(offset).limit(limit)
    )

    return users.all()