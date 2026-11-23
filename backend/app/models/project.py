
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    Uuid,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Основная информация
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Рабочая директория внутри среды выполнения SDK
    working_directory: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )

    # Дополнительные директории, доступные агенту
    additional_directories: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )

    # Общие инструкции для агента
    system_prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Конфигурация инструментов
    tools_preset: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {
            "type": "preset",
            "preset": "claude_code",
        },
        server_default=text(
            """'{"type":"preset","preset":"claude_code"}'::jsonb"""
        ),
    )

    # Автоматически одобряемые инструменты
    allowed_tools: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )

    # Запрещённые инструменты
    disallowed_tools: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )

    # Режим разрешений по умолчанию
    permission_mode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="default",
        server_default="default",
    )

    # Источники настроек Claude Code
    setting_sources: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: ["project", "local"],
        server_default=text(
            """'["project","local"]'::jsonb"""
        ),
    )

    # MCP-серверы и программные субагенты
    mcp_servers: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    agents: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
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
