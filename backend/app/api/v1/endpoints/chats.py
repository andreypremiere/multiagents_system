from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.dependencies import get_current_user
from backend.app.core.database import get_db
from backend.app.models.chat import Chat
from backend.app.models.user import User
from backend.app.schemas.chat import ChatCreate, ChatOut, ChatUpdate
from backend.app.services.chat import ChatService

router = APIRouter(tags=["chats"])


@router.get("/projects/{project_id}/chats", response_model=list[ChatOut])
async def list_chats(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Chat]:
    """Возвращает чаты проекта текущего пользователя."""
    return await ChatService().list_chats(db, current_user.id, project_id)


@router.post("/projects/{project_id}/chats", response_model=ChatOut, status_code=201)
async def create_chat(
    project_id: uuid.UUID,
    payload: ChatCreate | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Chat:
    """Создаёт чат в проекте. Без тела используются значения по умолчанию."""
    return await ChatService().create_chat(
        db, current_user.id, project_id, payload or ChatCreate()
    )


@router.get("/chats/{chat_id}", response_model=ChatOut)
async def read_chat(
    chat_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Chat:
    """Возвращает чат, если он принадлежит проекту текущего пользователя."""
    return await ChatService().get_chat(db, current_user.id, chat_id)


@router.patch("/chats/{chat_id}", response_model=ChatOut)
async def update_chat(
    chat_id: uuid.UUID,
    payload: ChatUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Chat:
    """Частично обновляет чат."""
    return await ChatService().update_chat(db, current_user.id, chat_id, payload)
