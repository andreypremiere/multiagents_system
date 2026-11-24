from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.crypto import decrypt_secret, encrypt_secret
from backend.app.models.provider_credential import ProviderCredential
from backend.app.repositories.provider_credential import ProviderCredentialRepository
from backend.app.schemas.provider_credential import (
    ProviderCredentialOut,
    ProviderCredentialUpsert,
)
from backend.app.services.errors import NotFoundError


def _mask_secret(secret: str) -> str:
    """Показывает только последние 4 символа. Короткие секреты не раскрываются целиком."""
    if len(secret) <= 8:
        return "••••"
    return f"••••{secret[-4:]}"


def _to_out(credential: ProviderCredential) -> ProviderCredentialOut:
    secret = decrypt_secret(credential.encrypted_secret)
    return ProviderCredentialOut(
        id=credential.id,
        provider=credential.provider,
        auth_type=credential.auth_type,
        masked_secret=_mask_secret(secret),
        is_active=credential.is_active,
        created_at=credential.created_at,
        updated_at=credential.updated_at,
    )


class ProviderCredentialService:
    """Бизнес-логика ключей провайдеров. Секреты хранятся только в зашифрованном виде."""

    def __init__(self, repository: ProviderCredentialRepository | None = None) -> None:
        self.repository = repository or ProviderCredentialRepository()

    async def list_credentials(
        self, db: AsyncSession, user_id: uuid.UUID
    ) -> list[ProviderCredentialOut]:
        credentials = await self.repository.list_by_user(db, user_id)
        return [_to_out(credential) for credential in credentials]

    async def upsert_credential(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        provider: str,
        payload: ProviderCredentialUpsert,
    ) -> ProviderCredentialOut:
        encrypted = encrypt_secret(payload.secret)
        credential = await self.repository.get_by_provider(db, user_id, provider)

        if credential is None:
            credential = await self.repository.add(
                db,
                ProviderCredential(
                    user_id=user_id,
                    provider=provider,
                    auth_type=payload.auth_type,
                    encrypted_secret=encrypted,
                ),
            )
        else:
            credential.auth_type = payload.auth_type
            credential.encrypted_secret = encrypted
            credential.is_active = True

        await db.commit()
        await db.refresh(credential)
        return _to_out(credential)

    async def delete_credential(
        self, db: AsyncSession, user_id: uuid.UUID, credential_id: uuid.UUID
    ) -> None:
        credential = await self.repository.get_by_id_for_user(db, user_id, credential_id)
        if credential is None:
            raise NotFoundError("Ключ не найден")
        await self.repository.delete(db, credential)
        await db.commit()
