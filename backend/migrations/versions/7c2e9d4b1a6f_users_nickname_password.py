"""users: replace key with nickname and hashed_password

Revision ID: 7c2e9d4b1a6f
Revises: 1afa636e7b88
Create Date: 2026-11-22 23:30:00.000000

Ревизия написана вручную. Перед `alembic upgrade head` нужно заполнить
nickname и hashed_password у существующих строк, см. backend/migrations/MIGRATION_NICKNAME.md.
Если остались строки с NULL, миграция останавливается с ошибкой и ничего не меняет.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "7c2e9d4b1a6f"
down_revision: Union[str, Sequence[str], None] = "1afa636e7b88"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Колонки добавляются через IF NOT EXISTS, чтобы шаг можно было выполнить
    # вручную заранее (см. инструкцию) без конфликта с этой ревизией.
    op.execute(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS nickname VARCHAR(50)"
    )
    op.execute(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS hashed_password VARCHAR(255)"
    )

    bind = op.get_bind()
    missing = bind.execute(
        sa.text(
            "SELECT count(*) FROM users "
            "WHERE nickname IS NULL OR hashed_password IS NULL"
        )
    ).scalar_one()
    if missing:
        raise RuntimeError(
            f"В таблице users {missing} строк без nickname или hashed_password. "
            "Заполните их по инструкции MIGRATION_NICKNAME.md и повторите миграцию."
        )

    op.alter_column("users", "nickname", existing_type=sa.String(50), nullable=False)
    op.alter_column(
        "users", "hashed_password", existing_type=sa.String(255), nullable=False
    )
    op.create_unique_constraint("uq_users_nickname", "users", ["nickname"])

    op.drop_constraint("users_key_key", "users", type_="unique")
    op.drop_column("users", "key")


def downgrade() -> None:
    # Внимание: пароли и никнеймы при откате теряются. В key пишется nickname
    # как временное значение, его нужно будет поменять вручную.
    op.add_column("users", sa.Column("key", sa.String(255), nullable=True))
    op.execute("UPDATE users SET key = nickname")
    op.alter_column("users", "key", existing_type=sa.String(255), nullable=False)
    op.create_unique_constraint("users_key_key", "users", ["key"])

    op.drop_constraint("uq_users_nickname", "users", type_="unique")
    op.drop_column("users", "hashed_password")
    op.drop_column("users", "nickname")
