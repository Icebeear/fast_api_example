from pydantic import BaseModel, Field
from typing import Annotated
from datetime import date

class Task(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=128)]
    description: Annotated[str | None, Field(default=None, max_length=1024)] 
    is_complete: bool = False 
    created_at: date 
    owner_id: int
