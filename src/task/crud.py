from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from src.task.models import Task
from src.task import schemas


async def create_task(task: schemas.Task, session: AsyncSession):
    query = insert(Task).values(**task.model_dump())
    await session.execute(query)
    await session.commit()
    return task


async def get_task_by_name(task_name: str, session: AsyncSession):
    query = select(Task).where(Task.name == task_name)
    result = await session.execute(query)
    return result.scalars().first()


async def get_tasks(session: AsyncSession, offset: int = 0, limit: int = 100):
    query = select(Task).offset(offset).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def get_task_by_id(task_id: int, session: AsyncSession):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return result.scalars().first()


async def update_task_by_id(task: schemas.Task, session: AsyncSession):
    task.is_complete = not task.is_complete
    await session.commit()
    return task 


async def delete_task(task: schemas.Task, session: AsyncSession):
    await session.delete(task)
    await session.commit()
    return {"response": f"Task with id {task.id} was successfully deleted"}