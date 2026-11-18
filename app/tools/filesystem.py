from pathlib import Path

from langchain_core.tools import tool

from app.config import WORKSPACE_PATH


def resolve_path(path: str) -> Path:
    target = (WORKSPACE_PATH / path).resolve()

    if not target.is_relative_to(WORKSPACE_PATH):
        raise PermissionError("Доступ за пределами workspace запрещён")

    return target


@tool
def read_file(path: str) -> str:
    """Читает содержимое файла. Путь указывается относительно workspace."""

    target = resolve_path(path)

    if not target.is_file():
        return f"Файл не найден: {path}"

    return target.read_text(encoding="utf-8")


@tool
def write_file(path: str, content: str) -> str:
    """Создаёт новый файл или полностью перезаписывает существующий."""

    target = resolve_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    return f"Файл записан: {path}"


@tool
def edit_file(path: str, old_text: str, new_text: str) -> str:
    """
    Частично редактирует файл.
    Заменяет точное вхождение old_text на new_text.
    Требует ровно одного совпадения.
    """

    target = resolve_path(path)

    if not target.is_file():
        return f"Файл не найден: {path}"

    content = target.read_text(encoding="utf-8")

    count = content.count(old_text)

    if count == 0:
        return "Ошибка: исходный фрагмент не найден."

    if count > 1:
        return (
            f"Ошибка: найдено {count} совпадений. "
            "Уточни исходный фрагмент."
        )

    updated = content.replace(old_text, new_text, 1)
    target.write_text(updated, encoding="utf-8")

    return f"Файл успешно изменён: {path}"


@tool
def insert_into_file(
    path: str,
    marker: str,
    content: str,
    position: str = "after",
) -> str:
    """
    Вставляет текст относительно уникального маркера.
    position: before или after.
    """

    target = resolve_path(path)

    if not target.is_file():
        return f"Файл не найден: {path}"

    if position not in ("before", "after"):
        return "Ошибка: position должен быть before или after."

    original = target.read_text(encoding="utf-8")

    count = original.count(marker)

    if count != 1:
        return f"Ошибка: маркер должен встречаться ровно один раз. Найдено: {count}"

    if position == "after":
        updated = original.replace(
            marker, marker + content, 1
        )
    else:
        updated = original.replace(
            marker, content + marker, 1
        )

    target.write_text(updated, encoding="utf-8")

    return f"Текст вставлен в файл: {path}"


@tool
def list_files(path: str = ".") -> str:
    """Показывает структуру директории относительно workspace."""

    target = resolve_path(path)

    if not target.is_dir():
        return f"Директория не найдена: {path}"

    result = []

    for item in sorted(target.rglob("*")):
        if any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in item.parts):
            continue

        relative = item.relative_to(WORKSPACE_PATH)
        prefix = "[DIR] " if item.is_dir() else "[FILE] "

        result.append(prefix + str(relative))

    return "\n".join(result[:500]) or "Директория пуста."


@tool
def create_directory(path: str) -> str:
    """Создаёт директорию и все необходимые родительские директории."""

    target = resolve_path(path)
    target.mkdir(parents=True, exist_ok=True)

    return f"Директория создана: {path}"