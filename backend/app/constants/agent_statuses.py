from enum import Enum
from typing import TypedDict


class AgentStatus(str, Enum):
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    WAITING_FOR_INPUT = "waiting_for_input"
    WAITING_FOR_APPROVAL = "waiting_for_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    INTERRUPTED = "interrupted"


class AgentStatusOption(TypedDict):
    value: str
    label: str


AGENT_STATUS_OPTIONS: tuple[AgentStatusOption, ...] = (
    {"value": AgentStatus.IDLE.value, "label": "Ожидание"},
    {"value": AgentStatus.STARTING.value, "label": "Запуск"},
    {"value": AgentStatus.RUNNING.value, "label": "Выполняется"},
    {"value": AgentStatus.WAITING_FOR_INPUT.value, "label": "Ожидает ввода"},
    {"value": AgentStatus.WAITING_FOR_APPROVAL.value, "label": "Ожидает подтверждения"},
    {"value": AgentStatus.COMPLETED.value, "label": "Завершено"},
    {"value": AgentStatus.FAILED.value, "label": "Ошибка"},
    {"value": AgentStatus.CANCELLED.value, "label": "Отменено"},
    {"value": AgentStatus.INTERRUPTED.value, "label": "Прервано"},
)


ACTIVE_STATUSES = frozenset({
    AgentStatus.STARTING,
    AgentStatus.RUNNING,
    AgentStatus.WAITING_FOR_INPUT,
    AgentStatus.WAITING_FOR_APPROVAL,
})


TERMINAL_STATUSES = frozenset({
    AgentStatus.COMPLETED,
    AgentStatus.FAILED,
    AgentStatus.CANCELLED,
    AgentStatus.INTERRUPTED,
})