import asyncio
import os
from pathlib import Path

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AssistantMessage,
    ResultMessage,
    TextBlock, UserMessage,
)

# Загружаем .env из директории Python-файла
from dotenv import load_dotenv

load_dotenv(".env")

# Проверяем наличие ключа
if not os.getenv("ANTHROPIC_API_KEY"):
    raise RuntimeError("ANTHROPIC_API_KEY не найден в .env")

claude_options = ClaudeAgentOptions(
    # инструменты claude code по умолчанию
    tools={'type': 'preset', 'preset': 'claude_code'},
    # Инструменты для автоматического одобрения без запроса разрешения
    allowed_tools=['Edit', 'Write'],
    # определяет поведение для всех остальных инструментов https://code.claude.com/docs/en/tools-reference
    permission_mode='default',
    disallowed_tools=['Bash', 'PowerShell'],
    # Продолжать сессию
    continue_conversation=False,
    # # идентификатор сессии для возобновления
    resume='dee91e8c-b455-4704-82a6-bb855a5faccb',
    # session_id='e3bba005-a95d-4375-9570-b8931fc7b8bc',
    # количество агентских шагов
    # max_turns=20,
    max_budget_usd=1,
    model='claude-haiku-5-5',
    # структурированный ответ
    output_format=None,
    cwd=r'E:\multiagents_system',
    add_dirs=[],
    # Программно определенные агенты
    agents=None,
    # env={
    #     "ANTHROPIC_API_KEY": api_key,
    # },
)


async def main():
    # Создаём интерактивную сессию Claude Code.

    client = ClaudeSDKClient(options=claude_options)
    try:
        await client.connect()
        print("Claude SDK connected\n")
    except Exception as e:
        print(f"Не удалось установить соединение с клиентом: {e}")
        return

    # Первое сообщение
    prompt = """1. Согласен 
    2. пока оставить моки, потом отдельной задачей будем делать чат. 
    3. как лучше будет, делай по аналогии других уже готовых апи. 
    4. давай б. 
    5. оставь пока обычные строки без валидации. 
    6. удали с фронта, сейчас ориентуремся на бекенд. 
    7. да, пока не нужно это делать, потом также отдельной задачей. 
    8. Таблицы уже необходимые все созданы, не нужны никакие миграции. 
    9. да, можно удалить. 
    Приступай к реализации"""



    print(f"You: {prompt}\n")

    await client.query(
        prompt,
        # session_id=session_id
    )

    async for message in client.receive_response():
        if isinstance(message, UserMessage):
            print(f'[uuid: {message.uuid}]user message: {message.content}')
        if isinstance(message, AssistantMessage):
            print(f'[uuid: {message.uuid}] message: {message}')
            for block in message.content:
                print(f'[uuid: {message.uuid}] block: {block}')
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")

        elif isinstance(message, ResultMessage):
            print("\n--- Request completed ---")
            print(f"subtype: {message.subtype}")
            print(f"usage: {message.usage}")
            print("Session ID:", message.session_id)
            print("Duration:", message.duration_ms, "ms")
            print("Cost:", message.total_cost_usd)

    try:
        await client.disconnect()
    except Exception as e:
        print('Не удалось разъеденить соединение')


if __name__ == "__main__":
    asyncio.run(main())
