from enum import Enum
from typing import TypedDict


class ToolName(str, Enum):
    # Работа с файлами
    READ = "Read"
    WRITE = "Write"
    EDIT = "Edit"
    GLOB = "Glob"
    GREP = "Grep"

    # Выполнение команд
    BASH = "Bash"
    KILL_SHELL = "KillShell"

    # Работа с агентами и задачами
    AGENT = "Agent"
    TASK_CREATE = "TaskCreate"
    TASK_GET = "TaskGet"
    TASK_LIST = "TaskList"
    TASK_OUTPUT = "TaskOutput"
    TASK_STOP = "TaskStop"

    # Планирование и взаимодействие
    TODO_WRITE = "TodoWrite"
    ASK_USER_QUESTION = "AskUserQuestion"
    EXIT_PLAN_MODE = "ExitPlanMode"

    # Интернет
    WEB_SEARCH = "WebSearch"
    WEB_FETCH = "WebFetch"

    # Дополнительные инструменты
    NOTEBOOK_EDIT = "NotebookEdit"
    LSP = "LSP"
    SKILL = "Skill"


class ToolOption(TypedDict):
    value: str
    label: str
    category: str


CORE_TOOL_OPTIONS: tuple[ToolOption, ...] = (
    {"value": ToolName.READ.value, "label": "Чтение файлов", "category": "files"},
    {"value": ToolName.WRITE.value, "label": "Создание файлов", "category": "files"},
    {"value": ToolName.EDIT.value, "label": "Редактирование файлов", "category": "files"},
    {"value": ToolName.GLOB.value, "label": "Поиск файлов", "category": "files"},
    {"value": ToolName.GREP.value, "label": "Поиск по содержимому", "category": "files"},
    {"value": ToolName.BASH.value, "label": "Выполнение команд", "category": "terminal"},
    {"value": ToolName.KILL_SHELL.value, "label": "Остановка процессов", "category": "terminal"},
    {"value": ToolName.AGENT.value, "label": "Запуск субагентов", "category": "agents"},
    {"value": ToolName.TASK_CREATE.value, "label": "Создание задач", "category": "agents"},
    {"value": ToolName.TASK_GET.value, "label": "Получение задачи", "category": "agents"},
    {"value": ToolName.TASK_LIST.value, "label": "Список задач", "category": "agents"},
    {"value": ToolName.TASK_OUTPUT.value, "label": "Результат задачи", "category": "agents"},
    {"value": ToolName.TASK_STOP.value, "label": "Остановка задачи", "category": "agents"},
    {"value": ToolName.TODO_WRITE.value, "label": "Список дел", "category": "planning"},
    {"value": ToolName.ASK_USER_QUESTION.value, "label": "Вопрос пользователю", "category": "interaction"},
    {"value": ToolName.EXIT_PLAN_MODE.value, "label": "Завершение планирования", "category": "planning"},
    {"value": ToolName.WEB_SEARCH.value, "label": "Поиск в интернете", "category": "web"},
    {"value": ToolName.WEB_FETCH.value, "label": "Получение веб-страниц", "category": "web"},
    {"value": ToolName.NOTEBOOK_EDIT.value, "label": "Редактирование Notebook", "category": "files"},
    {"value": ToolName.LSP.value, "label": "Language Server Protocol", "category": "development"},
    {"value": ToolName.SKILL.value, "label": "Вызов Skills", "category": "agents"},
)


# Имена MCP-инструментов имеют вид:
# mcp__<server_name>__<tool_name>
MCP_TOOL_PREFIX = "mcp__"


def is_mcp_tool(tool_name: str) -> bool:
    """Проверяет, является ли инструмент MCP-инструментом."""
    return tool_name.startswith(MCP_TOOL_PREFIX)