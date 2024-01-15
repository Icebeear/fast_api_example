from fastapi import Depends, HTTPException, Path, Query, Body, APIRouter, status
from src.task import schemas
from typing import Annotated
from sqlalchemy.orm import Session
from src.settings.database import get_async_session
from fastapi.responses import JSONResponse
from src.task import crud
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Tasks"], prefix="/tasks")

from src.auth.crud import get_user_by_id

@router.post("/add", response_model=schemas.TaskCreate)
async def create_task(task: schemas.TaskCreate, session: AsyncSession = Depends(get_async_session)):
    new_task = await crud.get_task_by_name(task.name, session)
    if new_task:
        raise HTTPException(status_code=404, detail="Task with this name already exists")
    owner = await get_user_by_id(task.owner_id, session)
    if not owner:
        raise HTTPException(status_code=404, detail=f"User with id {task.owner_id} not found")
    task = await crud.create_task(task, session)
    task = jsonable_encoder(task)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"Task": task})


@router.get("/", response_model=list[schemas.TaskCreate])
async def get_tasks(session: AsyncSession = Depends(get_async_session), offset: int = 0, limit: int = 100):
    tasks = await crud.get_tasks(session, offset=offset, limit=limit)
    return tasks    


@router.get("/{task_id}", response_model=schemas.TaskCreate)
async def get_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    task = await crud.get_task_by_id(task_id, session)
    return task 


@router.put("/{task_id}", response_model=schemas.TaskCreate)
async def update_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    task = await crud.get_task_by_id(task_id, session)
    await crud.update_task_by_id(task, session)
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    task = await crud.get_task_by_id(task_id, session)
    result = await crud.delete_task(task, session)
    return result
