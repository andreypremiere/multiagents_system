
import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Название чата
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        default="Новый чат",
        server_default="Новый чат",
    )

    # Модель Claude
    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Уровень глубины рассуждений
    effort: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # Лимиты по умолчанию для запросов этого чата
    max_turns: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    max_budget_usd: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # Переопределения настроек проекта
    permission_mode: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # None означает наследование настроек проекта
    allowed_tools_override: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Дополнительные запреты чата
    disallowed_tools_extra: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )

    # Настройки extended thinking
    thinking: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Дополнительные инструкции чата
    system_prompt_append: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Идентификатор сессии Claude Code SDK
    sdk_session_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        unique=True,
    )

    # active / archived
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="active",
        server_default="active",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    last_message_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
