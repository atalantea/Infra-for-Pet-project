from sqlalchemy.orm import Mapped

from app.models.base_model import Base


class CategoryORM(Base):
    __tablename__ = "categories"

    title: Mapped[str]
