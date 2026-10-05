from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.repositories.category import CategoryRepository
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryNotFoundError(Exception):
    pass


class CategoryService:
    """Ключевые операции с задачами, включая бизнес-логику, валидацию и прочее"""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repository = CategoryRepository(db)
        return

    async def list_categories(self) -> list[CategoryRead]:
        categories = await self.repository.get_all()
        return [CategoryRead.model_validate(category) for category in categories]

    async def create_category(self, payload: CategoryCreate) -> CategoryRead:
        category = await self.repository.create(title=payload.title)
        await self.db.commit()
        return CategoryRead.model_validate(category)

    async def update_category(self, category_id: str, payload: CategoryUpdate) -> CategoryRead:
        category = await self.repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError

        category.title = payload.title

        await self.db.commit()
        return CategoryRead.model_validate(category)

    async def delete_category(self, category_id: str) -> None:
        category = await self.repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError

        await self.repository.delete(category)
        await self.db.commit()
        return
