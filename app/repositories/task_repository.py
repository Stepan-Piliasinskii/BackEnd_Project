from sqlalchemy.orm import Session
from app.repositories.models.task_orm import TaskORM

class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[TaskORM]:
        return self.db.query(TaskORM).all()

    def create(self, title: str) -> TaskORM:
        task = TaskORM(title=title)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def set_done(self, task_id: int) -> TaskORM | None:
        task = self.db.get(TaskORM, task_id)
        if task is None:
            return None
        task.done = True
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.db.get(TaskORM, task_id)
        if task is None:
            return False
        self.db.delete(task)
        self.db.commit()
        return True