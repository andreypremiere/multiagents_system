from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.project import Project
from backend.app.repositories.project import ProjectRepository
from backend.app.schemas.project import ProjectCreate, ProjectUpdate
from backend.app.services.errors import NotFoundError


class ProjectService:
    """Бизнес-логика проектов. Все операции ограничены владельцем."""

    def __init__(self, repository: ProjectRepository | None = None) -> None:
        self.repository = repository or ProjectRepository()

    async def list_projects(self, db: AsyncSession, user_id: uuid.UUID) -> list[Project]:
        return await self.repository.list_by_user(db, user_id)

    async def get_project(
        self, db: AsyncSession, user_id: uuid.UUID, project_id: uuid.UUID
    ) -> Project:
        project = await self.repository.get_by_id_for_user(db, user_id, project_id)
        if project is None:
            raise NotFoundError("Проект не найден")
        return project

    async def create_project(
        self, db: AsyncSession, user_id: uuid.UUID, payload: ProjectCreate
    ) -> Project:
        data = payload.model_dump(exclude_none=True, mode="json")
        project = await self.repository.add(db, Project(user_id=user_id, **data))
        await db.commit()
        return project

    async def update_project(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        project_id: uuid.UUID,
        payload: ProjectUpdate,
    ) -> Project:
        project = await self.get_project(db, user_id, project_id)
        data = payload.model_dump(exclude_unset=True, exclude_none=True, mode="json")
        for field, value in data.items():
            setattr(project, field, value)
        await db.commit()
        await db.refresh(project)
        return project
