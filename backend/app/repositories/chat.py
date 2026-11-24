from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.chat import Chat


class ChatRepository:
    """Доступ к таблице chats. SQL не должен утекать выше этого слоя."""

    async def list_by_project(self, db: AsyncSession, project_id: uuid.UUID) -> list[Chat]:
        result = await db.execute(
            select(Chat).where(Chat.project_id == project_id).order_by(Chat.created_at)
        )
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, chat_id: uuid.UUID) -> Chat | None:
        return await db.get(Chat, chat_id)

    async def add(self, db: AsyncSession, chat: Chat) -> Chat:
        db.add(chat)
        await db.flush()
        await db.refresh(chat)
        return chat
