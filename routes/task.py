from typing import List
from datetime import datetime
from utils.db_util import get_db
from utils.jwt_util import verify_token
from schemas.task import TaskCreate, TaskSyncModel
from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter(prefix="/task", tags=["Task Management"])


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate, db=Depends(get_db), user_data: dict = Depends(verify_token)
):
    try:
        userId = user_data.get("user")["id"]
        db_user = await db.user.find_unique(where={"id": userId})
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id"
            )
        data = {}
        if task.dueAt:
            data = {
                "title": task.title,
                "description": task.description,
                "hexColor": task.hexColor,
                "dueAt": datetime.fromisoformat(task.dueAt),
                "uid": db_user.id,
            }
        else:
            data = {
                "title": task.title,
                "description": task.description,
                "hexColor": task.hexColor,
                "uid": db_user.id,
            }
        created_task = await db.task.create(data=data)
        if not created_task:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create task",
            )
        return created_task
    except HTTPException:
        raise
    except Exception as e:
        print(f"Task Creation Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.get("/list", status_code=status.HTTP_200_OK)
async def list_all_task(db=Depends(get_db), user_data: dict = Depends(verify_token)):
    try:
        userId = user_data.get("user")["id"]
        db_user = await db.user.find_unique(where={"id": userId})
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id"
            )
        tasks = await db.task.find_many(where={"uid": db_user.id})
        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no tasks found for this user!",
            )
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        print(f"Task retrive Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    task_id: str, db=Depends(get_db), user_data: dict = Depends(verify_token)
):
    try:
        userId = user_data.get("user")["id"]
        db_user = await db.user.find_unique(where={"id": userId})
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not authenticate"
            )
        task = await db.task.find_unique(where={"id": task_id, "uid": db_user.id})
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user",
            )
        await db.task.delete(where={"id": task.id})
        return {"detail": "Task deleted successfully", "success": True}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Task deletion Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post("sync/", status_code=status.HTTP_201_CREATED)
async def sync_tasks(
    tasks=List[TaskSyncModel],
    db=Depends(get_db),
    user_data: dict = Depends(verify_token),
):
    try:
        userId = user_data.get("user")["id"]
        db_user = await db.user.find_unique(where={"id": userId})
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not authenticate"
            )
        to_insert = []
        for t in tasks:
            to_insert.append(
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "hexColor": t.hexColor,
                    "uid": db_user.id,
                    "dueAt": datetime.fromisoformat(t.dueAt),
                    "createdAt": datetime.fromisoformat(t.createdAt),
                    "updatedAt": datetime.fromisoformat(t.updatedAt),
                }
            )
        inserted = await db.task.create_many(data=to_insert, skip_duplicates=False)
        if not inserted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to sync tasks",
            )
        return inserted
    except HTTPException:
        raise
    except Exception as e:
        print(f"Task Syncing Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
