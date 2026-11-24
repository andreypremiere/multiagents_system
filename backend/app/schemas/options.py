from __future__ import annotations

from pydantic import BaseModel


class OptionOut(BaseModel):
    """Один вариант для выпадающего списка."""

    value: str
    label: str
    description: str | None = None
    dangerous: bool | None = None
    category: str | None = None


class OptionsOut(BaseModel):
    """Константные списки, которые фронтенд получает одним запросом."""

    agent_models: list[OptionOut]
    permission_modes: list[OptionOut]
    effort_levels: list[OptionOut]
    tool_options: list[OptionOut]
    default_model: str
    default_permission_mode: str
    default_effort: str
