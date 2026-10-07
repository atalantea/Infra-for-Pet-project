from pydantic import BaseModel, ConfigDict


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str


class CategoryCreate(BaseModel):
    title: str


class CategoryUpdate(BaseModel):
    title: str
