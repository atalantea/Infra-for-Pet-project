from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class Task(BaseModel):
    """Модель задачи"""

    id: str
    title: str
    completed: bool = False


class TaskCreate(BaseModel):
    title: str


tasks: list[Task] = []


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    """Получить список задач"""
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    """Создать новую задачу"""
    task = Task(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task
