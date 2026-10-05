from fastapi import APIRouter

from app.api.routers.tasks import router as tasks_router
from app.api.routers.categories import router as category_router
from app.api.routers.health import router as health_router

api_router = APIRouter()
api_router.include_router(tasks_router)
api_router.include_router(category_router)
api_router.include_router(health_router)
