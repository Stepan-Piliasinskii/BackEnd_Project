from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from app.api.models.task_models import TaskCreateRequest, TaskResponse

router = APIRouter()

def get_service(db: Session = Depends(get_db)) -> TaskService:
    repo = TaskRepository(db=db)
    return TaskService(repo=repo)

@router.get("/", response_model=list[TaskResponse])
def get_tasks(service: TaskService = Depends(get_service)):
    return service.get_all()

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreateRequest, service: TaskService = Depends(get_service)):
    return service.create(title=payload.title)

@router.patch("/{task_id}/done", response_model=TaskResponse)
def mark_done(task_id: int, service: TaskService = Depends(get_service)):
    task = service.set_done(task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, service: TaskService = Depends(get_service)):
    success = service.delete(task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")