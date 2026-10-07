from unittest.mock import AsyncMock

import pytest

from app.models.task_model import TaskORM
from app.schemas.task_schema import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskNotFoundError, TaskService


@pytest.mark.asyncio
async def test_list_tasks_returns_pydantic_models(
    service: TaskService,
    repository_mock: AsyncMock,
) -> None:
    # Имитируем, что метод get_all репозитория вернет эти задачи
    repository_mock.get_all.return_value = [
        TaskORM(id="task-1", title="Изучить pytest", completed=False),
        TaskORM(id="task-2", title="Написать первый тест", completed=True),
    ]

    result = await service.list_tasks()

    assert result == [
        TaskRead(id="task-1", title="Изучить pytest", completed=False),
        TaskRead(id="task-2", title="Написать первый тест", completed=True),
    ]


@pytest.mark.asyncio
async def test_create_task_commits_created_task(
    service: TaskService,
    db_mock: AsyncMock,
    repository_mock: AsyncMock,
) -> None:
    created_task = TaskORM(id="task-1", title="Новая задача", completed=False)
    repository_mock.create.return_value = created_task

    result = await service.create_task(TaskCreate(title="Новая задача"))

    repository_mock.create.assert_called_once_with(title="Новая задача")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": "Новая задача",
        "completed": False,
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("payload", "expected_title", "expected_completed"),
    [
        pytest.param(
            TaskUpdate(title="Обновить заголовок"),  # payload
            "Обновить заголовок",  # expected_title
            False,  # expected_completed
        ),
        pytest.param(
            TaskUpdate(completed=True),  # payload
            "Старая задача",  # expected_title
            True,  # expected_completed
        ),
        pytest.param(
            TaskUpdate(title="Готово", completed=True),  # payload
            "Готово",  # expected_title
            True,  # expected_completed
        ),
    ],
)
async def test_update_task_updates_only_passed_fields(
    service: TaskService,
    db_mock: AsyncMock,
    repository_mock: AsyncMock,
    payload: TaskUpdate,
    expected_title: str,
    expected_completed: bool,
) -> None:
    task = TaskORM(id="task-1", title="Старая задача", completed=False)
    repository_mock.get_by_id.return_value = task

    result = await service.update_task("task-1", payload)

    repository_mock.get_by_id.assert_called_once_with(task_id="task-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": expected_title,
        "completed": expected_completed,
    }


@pytest.mark.asyncio
async def test_update_task_raises_when_task_not_found(
    service: TaskService,
    db_mock: AsyncMock,
    repository_mock: AsyncMock,
) -> None:
    repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFoundError):  # Должна произойти указанная ошибка
        await service.update_task("missing-task", TaskUpdate(title="Неважно"))

    db_mock.commit.assert_not_called()
