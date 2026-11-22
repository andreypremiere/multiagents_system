# Миграция: вход по nickname и паролю вместо key

Ревизия: `7c2e9d4b1a6f` (файл `backend/migrations/versions/7c2e9d4b1a6f_users_nickname_password.py`), предыдущая `1afa636e7b88`.

Что делает: удаляет колонку `key` (и её unique-констрейнт `users_key_key`), добавляет `nickname VARCHAR(50) NOT NULL UNIQUE` и `hashed_password VARCHAR(255) NOT NULL`.

Проблема: в существующих строках нет никнейма и пароля. Поэтому миграция не пройдёт, пока они не заполнены. Порядок ниже.

## 0. Резервная копия

```bash
docker exec postgres_db pg_dump -U app_user -d app_db > backup_before_nickname.sql
```

## 1. Добавить новые колонки как nullable

Можно выполнить вручную в psql или через `docker exec -it postgres_db psql -U app_user -d app_db`:

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS nickname VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS hashed_password VARCHAR(255);
```

## 2. Посмотреть существующих пользователей

```sql
SELECT id, name, key FROM users;
```

## 3. Заполнить nickname и hashed_password

Для каждого пользователя нужно выбрать никнейм (3–50 символов) и пароль (от 8 символов, не длиннее 72 байт в UTF-8). Хэш считается bcrypt. Пример скрипта, запускать из корня проекта в venv, где установлен `bcrypt`:

```python
# Файл лежит вне backend/, например в scratch/set_credentials.py.
import getpass
import bcrypt

password = getpass.getpass("Пароль: ")
print(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))
```

Затем в psql (подставьте реальные значения):

```sql
UPDATE users
SET nickname = 'andrey',
    hashed_password = '$2b$12$...вставьте_хэш...'
WHERE id = '00000000-0000-0000-0000-000000000000';
```

Вариант: если хотите, чтобы старый ключ доступа стал паролем, можно захэшировать значение `key` тем же способом. Это удобно, но тогда старый ключ остаётся в ходу как пароль, поэтому выбирайте осознанно.

Никнеймы должны быть уникальными, иначе шаг 5 упадёт.

## 4. Проверить, что пустых значений не осталось

```sql
SELECT count(*) FROM users WHERE nickname IS NULL OR hashed_password IS NULL;
-- должно вернуть 0
```

## 5. Применить миграцию

Из папки `backend/` (там лежит `alembic.ini`), с активным venv:

```bash
alembic upgrade head
```

Миграция сама проверит строки с NULL и остановится с ошибкой, если они остались. Тогда ничего не меняется, вернитесь к шагу 3.

## 6. Проверка

```sql
\d users
SELECT id, nickname, name FROM users;
```

Колонка `key` должна исчезнуть, `nickname` и `hashed_password` стать `NOT NULL`.

## Откат

```bash
alembic downgrade 1afa636e7b88
```

Внимание: откат теряет никнеймы и пароли. В `key` пойдёт значение никнейма, его нужно поменять вручную. Для восстановления лучше использовать резервную копию из шага 0.

## Установка зависимостей

После обновления `requirements.txt` установите `bcrypt`:

```bash
pip install -r backend/requirements.txt
```
