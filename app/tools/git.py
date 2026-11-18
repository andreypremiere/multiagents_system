import subprocess

from langchain_core.tools import tool

from app.config import WORKSPACE_PATH


def run_git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=WORKSPACE_PATH,
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.returncode != 0:
        return f"Git error:\n{result.stderr}"

    return result.stdout or "Операция выполнена."


@tool
def git_status() -> str:
    """Показывает состояние Git-репозитория."""

    return run_git("status", "--short", "--branch")


@tool
def git_create_branch(branch_name: str) -> str:
    """Создаёт новую Git-ветку и переключается на неё."""

    return run_git("switch", "-c", branch_name)


@tool
def git_commit(message: str) -> str:
    """Создаёт коммит всех подготовленных к коммиту изменений."""

    status = run_git("status", "--porcelain")

    if status.startswith("Git error"):
        return status

    if not status.strip():
        return "Нет изменений для коммита."

    result = run_git("add", "-A")

    if result.startswith("Git error"):
        return result

    return run_git("commit", "-m", message)


@tool
def git_log(limit: int = 10) -> str:
    """Показывает последние коммиты."""

    limit = max(1, min(limit, 50))

    return run_git(
        "log",
        f"-{limit}",
        "--oneline",
        "--decorate",
    )


@tool
def git_rollback_files(paths: list[str]) -> str:
    """
    Откатывает указанные файлы к состоянию последнего коммита.
    Не затрагивает остальные файлы.
    Операция уничтожает незакоммиченные изменения в указанных файлах.
    """

    if not paths:
        return "Не указаны файлы для отката."

    validated = []

    for path in paths:
        if not path or path.startswith("-"):
            return f"Недопустимый путь: {path}"

        validated.append(path)

    return run_git(
        "restore",
        "--worktree",
        "--",
        *validated,
    )