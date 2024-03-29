from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from src.auth import utils
from src.auth.models import User
from src.auth import schemas

from src.task.models import Task

async def create_user(user: schemas.User, session: AsyncSession):
    user.password = utils.get_password_hash(user.password)
    query = insert(User).values(**user.model_dump())
    await session.execute(query)
    await session.commit()
    return user


async def get_user_by_name(username: str, session: AsyncSession):
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    return result.scalars().first()
    

async def get_user_by_email(email: str, session: AsyncSession):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    return result.scalars().first()


async def get_users(session: AsyncSession, offset: int = 0, limit: int = 100):
    query = select(User).offset(offset).limit(limit)
    result = session.execute(query)
    return result.scalars().all()


async def get_user_by_id(user_id: int, session: AsyncSession):
    query = select(User).where(User.id == user_id)
    user = await session.execute(query)  
    if not user:
        raise HTTPException(status_code=404, detail=f"user {user_id} not found")
    return user 
    

async def get_all_user_tasks(user_id, session: AsyncSession):
    query = select(Task).where(Task.owner_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


def delete_user(user: schemas.User, session: AsyncSession):
    session.delete(user)
    session.commit()
    return {"response": f"user with id {user.id} was deleted succesfully"}
