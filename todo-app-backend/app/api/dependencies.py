from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.category_service import CategoryService
from app.services.task_service import TaskService


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(db)


def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(db)
