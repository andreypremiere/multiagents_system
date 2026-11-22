from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from backend.app.core.config import settings


def hash_password(password: str) -> str:
    """Возвращает bcrypt-хэш пароля в виде строки."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Сравнивает пароль с bcrypt-хэшем. Возвращает False при любой ошибке формата."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(
    user_id: uuid.UUID,
    nickname: str,
    name: str,
) -> tuple[str, int]:
    """Выпускает access-JWT с id, nickname и name пользователя.

    Возвращает пару (токен, время жизни в секундах).
    """
    now = datetime.now(timezone.utc)
    expires_in = settings.JWT_ACCESS_TOKEN_MINUTES * 60

    payload: dict[str, Any] = {
        "id": str(user_id),
        "nickname": nickname,
        "name": name,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
        "jti": str(uuid.uuid4()),
        "typ": "access",
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )

    return token, expires_in


def decode_access_token(token: str) -> dict[str, Any]:
    """Проверяет подпись и срок действия токена и возвращает payload.

    Бросает jwt.InvalidTokenError, если токен невалиден или просрочен.
    """
    return jwt.decode(
        token,
        settings.JWT_SECRET.get_secret_value(),
        algorithms=[settings.JWT_ALGORITHM],
    )


print(hash_password('AcOS4sO1a-ep'))