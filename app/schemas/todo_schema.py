from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, timezone

class TodoCreate(BaseModel):
    title: str = Field(..., title='Título', min_length=3, max_length=50)
    description: str = Field(..., title='Descrição', min_length=3, max_length=150)
    status: Optional[bool] = False

class Todo(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[bool] = False

class TodoDetail(BaseModel):
    todo_id: UUID
    status: bool
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = False

