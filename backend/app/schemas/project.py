from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.constants.permission_modes import PermissionMode


class ProjectCreate(BaseModel):
    """Тело запроса на создание проекта."""

    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    working_directory: str = Field(min_length=1, max_length=1024)
    system_prompt: str | None = None
    permission_mode: PermissionMode = PermissionMode.DEFAULT
    additional_directories: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    disallowed_tools: list[str] = Field(default_factory=list)


class ProjectUpdate(BaseModel):
    """Частичное обновление проекта. Передаются только изменяемые поля."""

    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    working_directory: str | None = Field(default=None, min_length=1, max_length=1024)
    system_prompt: str | None = None
    permission_mode: PermissionMode | None = None
    additional_directories: list[str] | None = None
    allowed_tools: list[str] | None = None
    disallowed_tools: list[str] | None = None
    is_archived: bool | None = None


class ProjectOut(BaseModel):
    """Публичные поля проекта."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    working_directory: str
    additional_directories: list[str]
    system_prompt: str | None
    permission_mode: str
    allowed_tools: list[str]
    disallowed_tools: list[str]
    is_archived: bool
    created_at: datetime
    updated_at: datetime
