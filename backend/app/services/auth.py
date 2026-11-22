from __future__ import annotations

import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from backend.app.models.user import User
from backend.app.repositories.user import UserRepository

# Хэш заглушки: если пользователя с таким никнеймом нет, всё равно выполняем
# проверку пароля, чтобы время ответа не выдавало существование никнейма.
_DUMMY_HASH = hash_password(secrets.token_urlsafe(32))


class InvalidCredentialsError(Exception):
    """Никнейм не найден или пароль не совпадает."""


class AuthService:
    """Бизнес-логика входа по никнейму и паролю."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def login(
        self, db: AsyncSession, nickname: str, password: str
    ) -> tuple[User, str, int]:
        user = await self.repository.get_by_nickname(db, nickname.strip())

        password_ok = verify_password(
            password,
            user.hashed_password if user is not None else _DUMMY_HASH,
        )

        # Одна и та же ошибка для "нет пользователя" и "неверный пароль".
        if user is None or not password_ok:
            raise InvalidCredentialsError

        token, expires_in = create_access_token(user.id, user.nickname, user.name)
        return user, token, expires_in
