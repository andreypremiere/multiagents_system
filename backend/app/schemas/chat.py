from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from backend.app.constants.agent_models import DEFAULT_MODEL, AgentModel
from backend.app.constants.effort_levels import DEFAULT_EFFORT, EffortLevel
from backend.app.constants.permission_modes import PermissionMode


class ChatCreate(BaseModel):
    """Тело запроса на создание чата. Все поля необязательны, кроме значений по умолчанию."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    model: AgentModel = AgentModel(DEFAULT_MODEL)
    effort: EffortLevel = EffortLevel(DEFAULT_EFFORT)
    max_turns: int | None = Field(default=None, ge=1)
    max_budget_usd: float | None = Field(default=None, ge=0)
    permission_mode: PermissionMode | None = None


class ChatUpdate(BaseModel):
    """Частичное обновление чата."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    model: AgentModel | None = None
    effort: EffortLevel | None = None
    max_turns: int | None = Field(default=None, ge=1)
    max_budget_usd: float | None = Field(default=None, ge=0)
    permission_mode: PermissionMode | None = None
    status: Literal["active", "archived"] | None = None


class ChatOut(BaseModel):
    """Публичные поля чата. Идентификатор сессии SDK наружу не отдаётся."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    model: str
    effort: str | None
    max_turns: int | None
    max_budget_usd: float | None
    permission_mode: str | None
    allowed_tools_override: list[str] | None
    disallowed_tools_extra: list[str]
    thinking: dict | None
    system_prompt_append: str | None
    status: str
    created_at: datetime
    updated_at: datetime
    last_message_at: datetime | None
