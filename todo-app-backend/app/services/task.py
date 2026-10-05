from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.repositories.task import TaskRepository
from sqlalchemy.ext.asyncio import AsyncSession


class TaskNotFoundError(Exception):
    pass


class TaskService:
    """Ключевые операции с задачами, включая бизнес-логику, валидацию и прочее"""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repository = TaskRepository(db)
        return

    async def list_tasks(self) -> list[TaskRead]:
        tasks = await self.repository.get_all()
        return [TaskRead.model_validate(task) for task in tasks]

    async def create_task(self, payload: TaskCreate) -> TaskRead:
        task = await self.repository.create(title=payload.title)
        await self.db.commit()
        return TaskRead.model_validate(task)

    async def update_task(self, task_id: str, payload: TaskUpdate) -> TaskRead:
        task = await self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError

        if payload.title is not None:
            task.title = payload.title
        if payload.completed is not None:
            task.completed = payload.completed

        await self.db.commit()
        return TaskRead.model_validate(task)

    async def delete_task(self, task_id: str) -> None:
        task = await self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError

        await self.repository.delete(task)
        await self.db.commit()
        return
