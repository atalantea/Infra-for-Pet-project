from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import CategoryORM


class CategoryRepository:
    """Ключевые операции с таблицей tasks в БД"""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        return

    async def get_all(self) -> list[CategoryORM]:
        """Получить все записи categories"""
        categories = await self.db.scalars(select(CategoryORM))
        return list(categories.all())

    async def get_by_id(self, category_id: str) -> CategoryORM | None:
        """Получить запись category по id"""
        return await self.db.get(CategoryORM, category_id)

    async def create(self, title: str) -> CategoryORM:
        """Создать запись category"""
        category = CategoryORM(title=title, completed=False)
        self.db.add(category)
        return category

    async def delete(self, category: CategoryORM) -> None:
        """Удалить запись category"""
        await self.db.delete(category)
        return
