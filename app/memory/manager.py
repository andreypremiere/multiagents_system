from app.database.postgres import get_memories


def build_memory_context(chat_id) -> str:
    memories = get_memories(chat_id)

    if not memories:
        return "Долгосрочная память пока пуста."

    result = []

    for category, content in memories:
        result.append(f"[{category}] {content}")

    return "\n".join(result)


def build_history_context(history) -> str:
    if not history:
        return "История диалога отсутствует."

    result = []

    for role, content in history:
        result.append(f"{role.upper()}: {content}")

    return "\n".join(result)