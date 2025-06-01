from utils.db_util import get_db
from fastapi import APIRouter, HTTPException, Depends
from utils.jwt_util import verify_token
from schemas.task import TaskCreate

router = APIRouter(prefix="/task", tags=["Task Management"])


@router.post("/add", status_code=201)
async def create_task(
    task: TaskCreate, db=Depends(get_db), user_data: dict = Depends(verify_token)
):
    try:
        userId = user_data.get("user")["id"]
        db_user = await db.user.find_unique(where={"id": userId})
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid user id")
        created_task = await db.task.create(
            data={
                "title": task.title,
                "description": task.description,
                "hexColor": task.hexColor,
                "dueAt": task.dueAt,
                "uid": db_user.id,
            }
        )
        if not created_task:
            raise HTTPException(status_code=500, detail="Failed to create task")
        return created_task
    except HTTPException:
        raise
    except Exception as e:
        print(f"Task Creation Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/list", status_code=200)
async def list_all_task(db=Depends(get_db), user_data: dict = Depends(verify_token)):
    try:
        userId = user_data.get("user")["id"]
        db_user = await db.user.find_unique(where={"id": userId})
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid user id")
        tasks = await db.task.find_many(where={"uid": db_user.id})
        if not tasks:
            raise HTTPException(status_code=404, detail="no tasks found for this user!")
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        print(f"Task retrive Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{task_id}", status_code=200)
async def delete_task(
    task_id: str, db=Depends(get_db), user_data: dict = Depends(verify_token)
):
    try:
        userId = user_data.get("user")["id"]
        db_user = await db.user.find_unique(where={"id": userId})
        if not db_user:
            raise HTTPException(status_code=400, detail="User not authenticate")
        task = await db.task.find_unique(where={"id": task_id, "uid": db_user.id})
        if not task:
            raise HTTPException(
                status_code=404, detail="Task not found or does not belong to user"
            )
        await db.task.delete(where={"id": task.id})
        return {"detail": "Task deleted successfully", "success": True}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Task deletion Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
