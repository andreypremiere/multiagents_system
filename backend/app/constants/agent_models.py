from enum import Enum
from typing import TypedDict


class AgentModel(str, Enum):
    OPUS_5_5 = "claude-opus-5-5"
    OPUS_5 = "claude-opus-5"

    SONNET_5_5 = "claude-sonnet-5-5"
    SONNET_5 = "claude-sonnet-5"

    HAIKU_5_5 = "claude-haiku-5-5"


class ModelOption(TypedDict):
    value: str
    label: str
    description: str
    family: str


MODEL_OPTIONS: tuple[ModelOption, ...] = (
    {
        "value": AgentModel.OPUS_5_5.value,
        "label": "Claude Opus 5.5",
        "description": "Флагманская модель для наиболее сложных задач",
        "family": "opus",
    },
    {
        "value": AgentModel.OPUS_5.value,
        "label": "Claude Opus 5",
        "description": "Модель Opus предыдущего поколения",
        "family": "opus",
    },
    {
        "value": AgentModel.SONNET_5_5.value,
        "label": "Claude Sonnet 5.5",
        "description": "Баланс производительности и скорости",
        "family": "sonnet",
    },
    {
        "value": AgentModel.SONNET_5.value,
        "label": "Claude Sonnet 5",
        "description": "Модель Sonnet предыдущего поколения",
        "family": "sonnet",
    },
    {
        "value": AgentModel.HAIKU_5_5.value,
        "label": "Claude Haiku 5.5",
        "description": "Быстрая и экономичная модель",
        "family": "haiku",
    },
)


DEFAULT_MODEL = AgentModel.HAIKU_5_5.value