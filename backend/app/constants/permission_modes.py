from enum import Enum
from typing import TypedDict


class PermissionMode(str, Enum):
    DEFAULT = "default"
    ACCEPT_EDITS = "acceptEdits"
    PLAN = "plan"
    DONT_ASK = "dontAsk"
    AUTO = "auto"
    BYPASS_PERMISSIONS = "bypassPermissions"


class PermissionModeOption(TypedDict):
    value: str
    label: str
    description: str
    dangerous: bool


PERMISSION_MODE_OPTIONS: tuple[PermissionModeOption, ...] = (
    {
        "value": PermissionMode.DEFAULT.value,
        "label": "По умолчанию",
        "description": "Стандартная проверка разрешений. Неподтверждённые действия требуют согласования",
        "dangerous": False,
    },
    {
        "value": PermissionMode.ACCEPT_EDITS.value,
        "label": "Автоматически принимать изменения",
        "description": "Автоматически разрешать изменения файлов, остальные действия проверять",
        "dangerous": False,
    },
    {
        "value": PermissionMode.PLAN.value,
        "label": "Планирование",
        "description": "Исследование задачи и составление плана без выполнения изменений",
        "dangerous": False,
    },
    {
        "value": PermissionMode.DONT_ASK.value,
        "label": "Не запрашивать подтверждение",
        "description": "Выполнять только заранее разрешённые действия, остальные отклонять",
        "dangerous": False,
    },
    {
        "value": PermissionMode.AUTO.value,
        "label": "Автоматическая проверка",
        "description": "Использовать классификатор безопасности для оценки действий",
        "dangerous": False,
    },
    {
        "value": PermissionMode.BYPASS_PERMISSIONS.value,
        "label": "Без ограничений",
        "description": "Обходить проверки разрешений. Использовать только в изолированной среде",
        "dangerous": True,
    },
)


DEFAULT_PERMISSION_MODE = PermissionMode.DEFAULT.value