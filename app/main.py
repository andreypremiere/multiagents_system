import uuid

from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import HumanMessage, AIMessage

from app.database.postgres import (
    init_database,
    get_connection,
    create_chat,
    chat_exists,
    create_task,
    update_task_status,
    save_message,
    get_chat_history,
    get_memories,
    get_task,
)

from app.agent.graph import (
    build_agent,
    build_system_message,
)

from app.memory.manager import (
    build_history_context,
    build_memory_context,
)

from app.config import (
    DATABASE_URL,
    WORKSPACE_PATH,
)


def new_id():
    return str(uuid.uuid4())


def get_chats():
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, title, updated_at
            FROM chats
            ORDER BY updated_at DESC
            """
        ).fetchall()


def touch_chat(chat_id):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE chats
            SET updated_at = NOW()
            WHERE id = %s
            """,
            (chat_id,),
        )


def get_task_thread_config(task_id):
    return {
        "configurable": {
            "thread_id": str(task_id),
        },
        "recursion_limit": 100,
    }


def get_response_content(result):
    messages = result.get("messages", [])

    for message in reversed(messages):
        if isinstance(message, AIMessage) and not message.tool_calls:
            return message.content

    return "Агент завершил выполнение без текстового ответа."


def run_task(agent, chat_id, user_message):

    task_id = new_id()

    history = get_chat_history(chat_id)
    memory = build_memory_context(chat_id)

    create_task(
        task_id,
        chat_id,
        user_message,
    )

    save_message(
        chat_id,
        task_id,
        "user",
        user_message,
    )

    messages = [
        build_system_message(
            str(WORKSPACE_PATH),
            "",
            memory,
        )
    ]

    for role, content in history:
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=user_message))

    print(f"\n[Task ID] {task_id}")
    print("[Agent] Выполнение задачи...\n")

    try:
        update_task_status(task_id, "running")
        result = agent.invoke(
            {"messages": messages},
            config=get_task_thread_config(task_id),
        )

        response = get_response_content(result)

        update_task_status(task_id, "completed")

        save_message(
            chat_id,
            task_id,
            "assistant",
            response if isinstance(response, str) else str(response),
        )

        touch_chat(chat_id)

        print("\n" + "=" * 60)
        print(response)
        print("=" * 60)

    except KeyboardInterrupt:
        update_task_status(
            task_id,
            "interrupted",
            "Выполнение прервано пользователем.",
        )

        print(
            f"\nЗадача прервана. Для продолжения: "
            f"/resume {task_id}"
        )

    except Exception as e:
        update_task_status(
            task_id,
            "interrupted",
            str(e),
        )

        print(f"\nОшибка выполнения: {e}")
        print(f"Попробуй восстановить задачу: /resume {task_id}")


def resume_task(agent, task_id):

    task = get_task(task_id)

    if not task:
        print("Задача не найдена.")
        return

    _, chat_id, status, user_message = task

    if status == "completed":
        print("Эта задача уже завершена.")
        return

    print(f"\nВосстановление задачи: {task_id}")

    try:
        result = agent.invoke(
            None,
            config=get_task_thread_config(task_id),
        )

        response = get_response_content(result)

        update_task_status(task_id, "completed")

        save_message(
            chat_id,
            task_id,
            "assistant",
            response if isinstance(response, str) else str(response),
        )

        touch_chat(chat_id)

        print("\n" + "=" * 60)
        print(response)
        print("=" * 60)

    except Exception as e:
        update_task_status(
            task_id,
            "interrupted",
            str(e),
        )

        print(f"Ошибка восстановления: {e}")


def print_help():
    print("""
Доступные команды:

/new [название]    Создать чат
/chats             Список чатов
/use ID            Переключиться на чат
/resume ID         Продолжить задачу
/help              Помощь
/exit              Выход

Любой другой ввод — новая задача для агента.
""")


def cli(agent):

    chat_id = new_id()

    create_chat(chat_id)

    print("\n" + "=" * 60)
    print("MULTI-AGENT SYSTEM — UNIVERSAL AGENT")
    print("=" * 60)
    print(f"Текущий Chat ID: {chat_id}")
    print("Введите /help для просмотра команд.")

    while True:

        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input == "/exit":
                print("Завершение работы.")
                break

            if user_input == "/help":
                print_help()
                continue

            if user_input.startswith("/new"):
                title = user_input[4:].strip() or "Новый чат"
                chat_id = new_id()
                create_chat(chat_id, title)

                print(f"Создан чат: {chat_id}")
                continue

            if user_input == "/chats":
                chats = get_chats()

                for cid, title, updated in chats:
                    print(f"{cid} | {title} | {updated}")

                continue

            if user_input.startswith("/use "):
                new_chat_id = user_input[5:].strip()

                if chat_exists(new_chat_id):
                    chat_id = new_chat_id
                    print(f"Текущий чат: {chat_id}")
                else:
                    print("Чат не найден.")

                continue

            if user_input.startswith("/resume "):
                task_id = user_input[8:].strip()
                resume_task(agent, task_id)
                continue

            run_task(
                agent,
                chat_id,
                user_input,
            )

        except KeyboardInterrupt:
            print("\nИспользуй /exit для завершения.")
        except EOFError:
            break


def main():

    print("Инициализация системы...")

    init_database()

    print("Подключение к PostgreSQL...")

    with PostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:

        checkpointer.setup()

        agent = build_agent(checkpointer)

        print("Агент готов.")

        cli(agent)


if __name__ == "__main__":
    main()