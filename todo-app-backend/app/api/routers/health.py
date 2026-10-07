from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health(session: AsyncSession = Depends(get_db)):
    return {"status": "ok", "env": settings.app_env}
