from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class User(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: str 
    full_name: str | None = None 
    email: EmailStr | None = None 
    active: bool = True 


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
