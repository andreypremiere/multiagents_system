import psycopg

from app.config import DATABASE_URL


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_database():
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id UUID PRIMARY KEY,
                    title TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id UUID PRIMARY KEY,
                    chat_id UUID NOT NULL REFERENCES chats(id),
                    status TEXT NOT NULL DEFAULT 'pending',
                    user_message TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW(),
                    error TEXT
                );
            """)

            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_chat_id
                ON tasks(chat_id);
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id BIGSERIAL PRIMARY KEY,
                    chat_id UUID NOT NULL REFERENCES chats(id),
                    task_id UUID REFERENCES tasks(id),
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_chat_id
                ON chat_messages(chat_id, id);
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id BIGSERIAL PRIMARY KEY,
                    chat_id UUID REFERENCES chats(id),
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    importance INTEGER DEFAULT 5,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

            conn.commit()


def create_chat(chat_id, title="Новый чат"):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO chats (id, title)
            VALUES (%s, %s)
            """,
            (chat_id, title),
        )


def chat_exists(chat_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM chats WHERE id = %s",
            (chat_id,),
        ).fetchone()

        return row is not None


def create_task(task_id, chat_id, message):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO tasks (id, chat_id, user_message)
            VALUES (%s, %s, %s)
            """,
            (task_id, chat_id, message),
        )


def update_task_status(task_id, status, error=None):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE tasks
            SET status = %s,
                error = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (status, error, task_id),
        )


def save_message(chat_id, task_id, role, content):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO chat_messages
            (chat_id, task_id, role, content)
            VALUES (%s, %s, %s, %s)
            """,
            (chat_id, task_id, role, content),
        )


def get_chat_history(chat_id, limit=30):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT role, content
            FROM (
                SELECT id, role, content
                FROM chat_messages
                WHERE chat_id = %s
                ORDER BY id DESC
                LIMIT %s
            ) AS recent
            ORDER BY id ASC
            """,
            (chat_id, limit),
        ).fetchall()

        return rows


def get_task(task_id):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, chat_id, status, user_message
            FROM tasks
            WHERE id = %s
            """,
            (task_id,),
        ).fetchone()


def save_memory(chat_id, category, content, importance=5):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO memories
            (chat_id, category, content, importance)
            VALUES (%s, %s, %s, %s)
            """,
            (chat_id, category, content, importance),
        )


def get_memories(chat_id, limit=20):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT category, content
            FROM memories
            WHERE chat_id IS NULL OR chat_id = %s
            ORDER BY importance DESC, updated_at DESC
            LIMIT %s
            """,
            (chat_id, limit),
        ).fetchall()

        return rows