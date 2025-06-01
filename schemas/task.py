from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: str
    hexColor: str
    dueAt: Optional[datetime] = None


class TaskSyncModel(BaseModel):
    id: str
    title: str
    description: str
    hexColor: str
    dueAt: datetime
    createdAt: datetime
    updatedAt: datetime
