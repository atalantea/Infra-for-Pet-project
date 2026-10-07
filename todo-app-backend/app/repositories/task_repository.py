from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_model import TaskORM


class TaskRepository:
    """Ключевые операции с таблицей tasks в БД"""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        return

    async def get_all(self) -> list[TaskORM]:
        """Получить все записи tasks"""
        tasks = await self.db.scalars(select(TaskORM))
        return list(tasks.all())

    async def get_by_id(self, task_id: str) -> TaskORM | None:
        """Получить запись task по id"""
        return await self.db.get(TaskORM, task_id)

    async def create(self, title: str) -> TaskORM:
        """Создать запись task"""
        task = TaskORM(title=title, completed=False)
        self.db.add(task)
        return task

    async def delete(self, task: TaskORM) -> None:
        """Удалить запись task"""
        await self.db.delete(task)
        return
