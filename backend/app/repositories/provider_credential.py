from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.provider_credential import ProviderCredential


class ProviderCredentialRepository:
    """Доступ к таблице provider_credentials. SQL не должен утекать выше этого слоя."""

    async def list_by_user(
        self, db: AsyncSession, user_id: uuid.UUID
    ) -> list[ProviderCredential]:
        result = await db.execute(
            select(ProviderCredential)
            .where(ProviderCredential.user_id == user_id)
            .order_by(ProviderCredential.created_at)
        )
        return list(result.scalars().all())

    async def get_by_provider(
        self, db: AsyncSession, user_id: uuid.UUID, provider: str
    ) -> ProviderCredential | None:
        result = await db.execute(
            select(ProviderCredential).where(
                ProviderCredential.user_id == user_id,
                ProviderCredential.provider == provider,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_id_for_user(
        self, db: AsyncSession, user_id: uuid.UUID, credential_id: uuid.UUID
    ) -> ProviderCredential | None:
        result = await db.execute(
            select(ProviderCredential).where(
                ProviderCredential.id == credential_id,
                ProviderCredential.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def add(
        self, db: AsyncSession, credential: ProviderCredential
    ) -> ProviderCredential:
        db.add(credential)
        await db.flush()
        await db.refresh(credential)
        return credential

    async def delete(self, db: AsyncSession, credential: ProviderCredential) -> None:
        await db.delete(credential)
        await db.flush()
