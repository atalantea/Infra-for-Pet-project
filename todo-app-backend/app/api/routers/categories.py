from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_category_service
from app.schemas.category_schema import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryNotFoundError, CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
async def get_categories(
    service: CategoryService = Depends(get_category_service),
) -> list[CategoryRead]:
    return await service.list_categories()


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
) -> CategoryRead:
    return await service.create_category(payload)


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_task(
    category_id: str,
    payload: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
) -> CategoryRead:
    try:
        return await service.update_category(category_id, payload)
    except CategoryNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    category_id: str,
    service: CategoryService = Depends(get_category_service),
) -> None:
    try:
        await service.delete_category(category_id)
    except CategoryNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
