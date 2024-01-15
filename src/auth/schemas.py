from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import Annotated
from src.task.schemas import TaskCreate


class User(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: str 
    full_name: str | None = None 
    email: EmailStr | None = None 
    active: bool = True 
    # tasks: list[TaskCreate] | None = []


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


