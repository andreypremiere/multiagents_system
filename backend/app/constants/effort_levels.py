from enum import Enum
from typing import TypedDict


class EffortLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    XHIGH = "xhigh"
    MAX = "max"


class EffortOption(TypedDict):
    value: str
    label: str
    description: str


EFFORT_OPTIONS: tuple[EffortOption, ...] = (
    {
        "value": EffortLevel.LOW.value,
        "label": "Низкий",
        "description": "Минимальные затраты на рассуждение, быстрый ответ",
    },
    {
        "value": EffortLevel.MEDIUM.value,
        "label": "Средний",
        "description": "Баланс скорости и глубины анализа",
    },
    {
        "value": EffortLevel.HIGH.value,
        "label": "Высокий",
        "description": "Более глубокий анализ сложных задач",
    },
    {
        "value": EffortLevel.XHIGH.value,
        "label": "Очень высокий",
        "description": "Расширенное рассуждение для сложных задач",
    },
    {
        "value": EffortLevel.MAX.value,
        "label": "Максимальный",
        "description": "Максимальный доступный уровень усилий модели",
    },
)


DEFAULT_EFFORT = EffortLevel.HIGH.value