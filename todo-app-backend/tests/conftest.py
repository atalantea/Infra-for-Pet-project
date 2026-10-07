from unittest.mock import AsyncMock

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


@pytest_asyncio.fixture
async def db_mock() -> AsyncMock:
    """Создаём мок сессии БД один раз и переиспользуем в тестах"""
    return AsyncMock(spec=AsyncSession)


@pytest_asyncio.fixture
async def repository_mock() -> AsyncMock:
    """Создаём мок TaskRepository один раз и переиспользуем в тестах"""
    return AsyncMock(spec=TaskRepository)


@pytest_asyncio.fixture
async def service(db_mock: AsyncMock, repository_mock: AsyncMock) -> TaskService:
    """Создаём TaskService один раз, чтобы переиспользовать в тестах"""
    task_service = TaskService(db_mock)
    task_service.repository = repository_mock
    return task_service
