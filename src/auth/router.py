from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.auth.schemas import Token, TokenData, User, UserInDB
from src.auth.utils import authenticate_user, create_access_token, get_current_active_user



from sqlalchemy.orm import Session
from src.settings.database import get_async_session

from src.auth import crud 

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from src.task import schemas

router = APIRouter(tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/register")
async def register_new_user(user: User, session: AsyncSession = Depends(get_async_session)):
    db_user = await crud.get_user_by_name(user.username, session)
    if db_user:
        raise HTTPException(status_code=404, detail="user with this name already exists")
    
    db_user = await crud.get_user_by_email(user.email, session)
    if db_user:
        raise HTTPException(status_code=404, detail="user with this email already exists")
    user = await crud.create_user(user, session)
    user = jsonable_encoder(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"user": user})


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    session: Session = Depends(get_async_session)
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@router.get("/users/me/tasks/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_async_session)
):
    tasks = await crud.get_all_user_tasks(current_user.id, session)
    return {"response": {"user": current_user, "tasks": tasks}}