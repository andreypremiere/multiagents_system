import subprocess

from langchain_core.tools import tool

from app.config import WORKSPACE_PATH


@tool
def docker_command(command: str) -> str:
    """
    Выполняет Docker CLI команду.
    Например: ps -a, images, compose ps, compose logs.
    """

    forbidden = [
        "system prune",
        "volume prune",
    ]

    if any(item in command for item in forbidden):
        return "Эта операция запрещена без отдельного подтверждения."

    try:
        result = subprocess.run(
            f"docker {command}",
            shell=True,
            cwd=WORKSPACE_PATH,
            capture_output=True,
            text=True,
            timeout=120,
        )

        return (
            f"Exit code: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )[-20000:]

    except Exception as e:
        return f"Docker error: {e}"