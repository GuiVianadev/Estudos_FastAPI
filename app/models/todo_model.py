from typing import Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link, before_event, Replace, Insert
from pydantic import Field
from .user_model import User

class Todo(Document):
    todo_id: UUID = Field(default_factory=uuid4, unique=True)
    status: bool = Field(default=False)
    title: str = Field(index=True)
    description: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    owner: Link[User]

    def __repr__(self) -> str:
        return f"<Todo {self.title}>"
  
    def __str__(self) -> str:
        return self.title
  
    def __hash__(self) -> int:
        return hash(self.title)
    
    def __eq__(self, other: object):
        if isinstance(other, Todo):
            return self.todo_id == other.todo_id
        return False
    
    @before_event([Replace, Insert])
    def sync_update_at(self):
        self.updated_at = datetime.now(timezone.utc)
