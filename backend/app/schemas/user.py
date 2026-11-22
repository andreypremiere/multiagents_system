from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator

# bcrypt обрабатывает не более 72 байт; проверяем в UTF-8 байтах, а не в символах.
BCRYPT_MAX_BYTES = 72


class LoginRequest(BaseModel):
    """Тело запроса на вход: никнейм и пароль."""

    nickname: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt_limit(cls, value: str) -> str:
        if len(value.encode("utf-8")) > BCRYPT_MAX_BYTES:
            raise ValueError(
                f"Пароль не должен превышать {BCRYPT_MAX_BYTES} байт в кодировке UTF-8"
            )
        return value


class UserOut(BaseModel):
    """Публичные поля пользователя. Пароль и его хэш сюда не попадают."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nickname: str
    name: str


class LoginResponse(BaseModel):
    """Ответ на успешный вход. Сам JWT лежит в httpOnly-cookie."""

    authenticated: bool = True
    token_type: str = "bearer"
    expires_in: int
    user: UserOut
