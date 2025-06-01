from datetime import datetime
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    hexColor: str
    dueAt: datetime


class TaskSyncModel(BaseModel):
    id: str
    title: str
    description: str
    hexColor: str
    dueAt: datetime
    createdAt: datetime
    updatedAt: datetime
