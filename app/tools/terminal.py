import subprocess

from langchain_core.tools import tool

from app.config import WORKSPACE_PATH


@tool
def execute_command(
    command: str,
    timeout: int = 120,
) -> str:
    """
    Выполняет команду терминала в рабочей директории workspace.
    Возвращает stdout и stderr.
    """

    timeout = max(1, min(timeout, 600))

    try:
        result = subprocess.run(
            command,
            cwd=WORKSPACE_PATH,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        output = (
            f"Exit code: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

        return output[-20000:]

    except subprocess.TimeoutExpired:
        return f"Команда превысила таймаут {timeout} секунд."

    except Exception as e:
        return f"Ошибка выполнения: {e}"