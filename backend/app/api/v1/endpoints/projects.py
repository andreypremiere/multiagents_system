from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.dependencies import get_current_user
from backend.app.core.database import get_db
from backend.app.models.project import Project
from backend.app.models.user import User
from backend.app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from backend.app.services.project import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectOut])
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Project]:
    """Возвращает неархивные проекты текущего пользователя."""
    return await ProjectService().list_projects(db, current_user.id)


@router.post("", response_model=ProjectOut, status_code=201)
async def create_project(
    payload: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Project:
    """Создаёт проект для текущего пользователя."""
    return await ProjectService().create_project(db, current_user.id, payload)


@router.get("/{project_id}", response_model=ProjectOut)
async def read_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Project:
    """Возвращает проект, если он принадлежит текущему пользователю."""
    return await ProjectService().get_project(db, current_user.id, project_id)


@router.patch("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: uuid.UUID,
    payload: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Project:
    """Частично обновляет проект. Архивация выполняется через is_archived."""
    return await ProjectService().update_project(db, current_user.id, project_id, payload)
