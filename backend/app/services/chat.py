from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.chat import Chat
from backend.app.models.project import Project
from backend.app.repositories.chat import ChatRepository
from backend.app.repositories.project import ProjectRepository
from backend.app.schemas.chat import ChatCreate, ChatUpdate
from backend.app.services.errors import NotFoundError


class ChatService:
    """Бизнес-логика чатов. Доступ к чату разрешён только владельцу проекта."""

    def __init__(
        self,
        chat_repository: ChatRepository | None = None,
        project_repository: ProjectRepository | None = None,
    ) -> None:
        self.chat_repository = chat_repository or ChatRepository()
        self.project_repository = project_repository or ProjectRepository()

    async def _get_owned_project(
        self, db: AsyncSession, user_id: uuid.UUID, project_id: uuid.UUID
    ) -> Project:
        project = await self.project_repository.get_by_id_for_user(db, user_id, project_id)
        if project is None:
            raise NotFoundError("Проект не найден")
        return project

    async def list_chats(
        self, db: AsyncSession, user_id: uuid.UUID, project_id: uuid.UUID
    ) -> list[Chat]:
        await self._get_owned_project(db, user_id, project_id)
        return await self.chat_repository.list_by_project(db, project_id)

    async def create_chat(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        project_id: uuid.UUID,
        payload: ChatCreate,
    ) -> Chat:
        await self._get_owned_project(db, user_id, project_id)
        data = payload.model_dump(exclude_none=True, mode="json")
        chat = await self.chat_repository.add(db, Chat(project_id=project_id, **data))
        await db.commit()
        return chat

    async def get_chat(
        self, db: AsyncSession, user_id: uuid.UUID, chat_id: uuid.UUID
    ) -> Chat:
        chat = await self.chat_repository.get_by_id(db, chat_id)
        if chat is None:
            raise NotFoundError("Чат не найден")
        await self._get_owned_project(db, user_id, chat.project_id)
        return chat

    async def update_chat(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        chat_id: uuid.UUID,
        payload: ChatUpdate,
    ) -> Chat:
        chat = await self.get_chat(db, user_id, chat_id)
        data = payload.model_dump(exclude_unset=True, exclude_none=True, mode="json")
        for field, value in data.items():
            setattr(chat, field, value)
        await db.commit()
        await db.refresh(chat)
        return chat
