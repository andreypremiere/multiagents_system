from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.app.api.dependencies import get_current_user
from backend.app.constants import (
    CORE_TOOL_OPTIONS,
    DEFAULT_EFFORT,
    DEFAULT_MODEL,
    DEFAULT_PERMISSION_MODE,
    EFFORT_OPTIONS,
    MODEL_OPTIONS,
    PERMISSION_MODE_OPTIONS,
)
from backend.app.models.user import User
from backend.app.schemas.options import OptionsOut

router = APIRouter(prefix="/options", tags=["options"])


@router.get("", response_model=OptionsOut)
async def read_options(
    current_user: User = Depends(get_current_user),
) -> OptionsOut:
    """Возвращает константные списки значений для выбора на фронтенде."""
    return OptionsOut(
        agent_models=list(MODEL_OPTIONS),
        permission_modes=list(PERMISSION_MODE_OPTIONS),
        effort_levels=list(EFFORT_OPTIONS),
        tool_options=list(CORE_TOOL_OPTIONS),
        default_model=DEFAULT_MODEL,
        default_permission_mode=DEFAULT_PERMISSION_MODE,
        default_effort=DEFAULT_EFFORT,
    )
