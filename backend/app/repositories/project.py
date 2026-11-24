from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.project import Project


class ProjectRepository:
    """Доступ к таблице projects. SQL не должен утекать выше этого слоя."""

    async def list_by_user(self, db: AsyncSession, user_id: uuid.UUID) -> list[Project]:
        result = await db.execute(
            select(Project)
            .where(Project.user_id == user_id, Project.is_archived.is_(False))
            .order_by(Project.created_at)
        )
        return list(result.scalars().all())

    async def get_by_id_for_user(
        self, db: AsyncSession, user_id: uuid.UUID, project_id: uuid.UUID
    ) -> Project | None:
        result = await db.execute(
            select(Project).where(Project.id == project_id, Project.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def add(self, db: AsyncSession, project: Project) -> Project:
        db.add(project)
        await db.flush()
        await db.refresh(project)
        return project
