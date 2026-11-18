import os
from langchain_openai import ChatOpenAI

from app.config import AGENT_TEMPERATURE


def get_llm(temperature: float = AGENT_TEMPERATURE) -> ChatOpenAI:
    """
    Возвращает языковую модель.
    Настройки провайдера и модели берутся из .env.
    """

    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")

    if not all([api_key, base_url, model]):
        raise RuntimeError(
            "В .env не заполнены LLM_API_KEY, "
            "LLM_BASE_URL или LLM_MODEL"
        )

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
    )