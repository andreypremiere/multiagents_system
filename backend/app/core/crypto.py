from __future__ import annotations

from cryptography.fernet import Fernet

from backend.app.core.config import settings

_fernet = Fernet(settings.CREDENTIALS_ENCRYPTION_KEY.get_secret_value().encode("utf-8"))


def encrypt_secret(plain: str) -> str:
    """Шифрует секрет провайдера перед записью в БД."""
    return _fernet.encrypt(plain.encode("utf-8")).decode("utf-8")


def decrypt_secret(token: str) -> str:
    """Расшифровывает секрет провайдера. Используется только на сервере."""
    return _fernet.decrypt(token.encode("utf-8")).decode("utf-8")
