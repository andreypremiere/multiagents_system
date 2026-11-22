from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.app.api.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
async def read_current_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Возвращает текущего пользователя по токену. Также проверка сессии."""
    return current_user
