from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProviderCredentialUpsert(BaseModel):
    """Тело запроса на создание или замену ключа провайдера."""

    auth_type: str = Field(default="api_key", min_length=1, max_length=50)
    secret: str = Field(min_length=1, max_length=4096)


class ProviderCredentialOut(BaseModel):
    """Публичные поля ключа провайдера. Сам секрет никогда не возвращается, только маска."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    provider: str
    auth_type: str
    masked_secret: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
