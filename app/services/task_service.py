from app.repositories.task_repository import TaskRepository
from app.api.models.task_models import TaskResponse

class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo

    def get_all(self) -> list[TaskResponse]:
        tasks = self.repo.get_all()
        return [TaskResponse.model_validate(task) for task in tasks]

    def create(self, title: str) -> TaskResponse:
        task = self.repo.create(title=title)
        return TaskResponse.model_validate(task)

    def set_done(self, task_id: int) -> TaskResponse | None:
        task = self.repo.set_done(task_id=task_id)
        if task is None:
            return None
        return TaskResponse.model_validate(task)

    def delete(self, task_id: int) -> bool:
        return self.repo.delete(task_id=task_id)