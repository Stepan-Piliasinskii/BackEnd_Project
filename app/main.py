from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routers import tasks
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task App")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])