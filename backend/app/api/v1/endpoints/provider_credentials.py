from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.dependencies import get_current_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.provider_credential import (
    ProviderCredentialOut,
    ProviderCredentialUpsert,
)
from backend.app.services.provider_credential import ProviderCredentialService

router = APIRouter(prefix="/provider-credentials", tags=["provider-credentials"])


@router.get("", response_model=list[ProviderCredentialOut])
async def list_provider_credentials(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[ProviderCredentialOut]:
    """Возвращает ключи провайдеров в замаскированном виде."""
    return await ProviderCredentialService().list_credentials(db, current_user.id)


@router.put("/{provider}", response_model=ProviderCredentialOut)
async def upsert_provider_credential(
    provider: str,
    payload: ProviderCredentialUpsert,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProviderCredentialOut:
    """Создаёт или заменяет ключ провайдера текущего пользователя."""
    return await ProviderCredentialService().upsert_credential(
        db, current_user.id, provider, payload
    )


@router.delete("/{credential_id}", status_code=204)
async def delete_provider_credential(
    credential_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Удаляет ключ провайдера текущего пользователя."""
    await ProviderCredentialService().delete_credential(db, current_user.id, credential_id)
