from contextlib import asynccontextmanager
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

DATABASE_URL = "postgresql+psycopg://admin:admin@db:5432/todo"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей таблиц БД"""

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class TaskORM(Base):
    """Модель для таблицы задачи в Базе Данных"""

    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategoryORM(Base):
    __tablename__ = "categories"

    title: Mapped[str]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


def get_db():
    """Функция для создания сессий с БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health/ready")
def ready(session: Session = Depends(get_db)):
    session.execute(text("SELECT title FROM categories LIMIT 0"))
    return {"status": "ok"}


class Task(BaseModel):
    """Модель задачи"""

    id: str
    title: str
    completed: bool = False


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class Category(BaseModel):
    id: str
    title: str


class CategoryCreate(BaseModel):
    title: str


class CategoryUpdate(BaseModel):
    title: str


def task_to_model(task: TaskORM) -> Task:
    """Конвертация объекта ORM в Pydantic"""
    return Task(id=task.id, title=task.title, completed=task.completed)


def category_to_model(category: CategoryORM) -> Category:
    """Конвертация объекта ORM в Pydantic"""
    return Category(id=category.id, title=category.title)


@app.get("/tasks", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)) -> list[Task]:
    """Получить список задач"""
    tasks = db.scalars(select(TaskORM)).all()
    return [task_to_model(task) for task in tasks]


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    """Создать новую задачу"""
    task = TaskORM(title=payload.title, completed=False)
    db.add(task)
    db.commit()
    return task_to_model(task)


@app.patch("/tasks/{id}", response_model=Task)
def update_task(id: str, payload: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    """
    Обновить существующую задачу
    id получаем из url
    payload получаем из тела запроса
    """
    task = db.get(TaskORM, id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    task.title = payload.title if payload.title is not None else task.title
    task.completed = (
        payload.completed if payload.completed is not None else task.completed
    )
    db.commit()
    return task_to_model(task)


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: str, db: Session = Depends(get_db)) -> None:
    """Удалить задачу"""
    task = db.get(TaskORM, id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    db.delete(task)
    db.commit()
    return


@app.get("/categories", response_model=list[Category])
def get_categories(db: Session = Depends(get_db)) -> list[Category]:
    categories = db.scalars(select(CategoryORM)).all()
    return [category_to_model(category) for category in categories]


@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)) -> Category:
    category = CategoryORM(title=payload.title)
    db.add(category)
    db.commit()
    return category_to_model(category)


@app.patch("/categories/{id}", response_model=Category)
def update_category(id: str, payload: CategoryUpdate, db: Session = Depends(get_db)) -> Category:
    category = db.get(CategoryORM, id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )
    category.title = payload.title
    db.commit()
    return category_to_model(category)


@app.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: str, db: Session = Depends(get_db)) -> None:
    category = db.get(CategoryORM, id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )
    db.delete(category)
    db.commit()
    return
