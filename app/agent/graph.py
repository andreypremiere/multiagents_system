from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

from app.llm.provider import get_llm
from app.config import AGENT_TEMPERATURE
from app.agent.prompts import SYSTEM_PROMPT

from app.tools.filesystem import (
    read_file,
    write_file,
    edit_file,
    insert_into_file,
    list_files,
    create_directory,
)

from app.tools.git import (
    git_status,
    git_create_branch,
    git_commit,
    git_log,
    git_rollback_files,
)

from app.tools.terminal import execute_command
from app.tools.docker import docker_command

from app.config import WORKSPACE_PATH


TOOLS = [
    read_file,
    write_file,
    edit_file,
    insert_into_file,
    list_files,
    create_directory,

    git_status,
    git_create_branch,
    git_commit,
    git_log,
    git_rollback_files,

    execute_command,
    docker_command,
]


def build_agent(checkpointer):

    llm = get_llm(temperature=AGENT_TEMPERATURE)
    llm_with_tools = llm.bind_tools(TOOLS)

    def assistant(state: MessagesState):

        response = llm_with_tools.invoke(state["messages"])

        return {
            "messages": [response]
        }

    builder = StateGraph(MessagesState)

    builder.add_node("assistant", assistant)

    builder.add_node(
        "tools",
        ToolNode(TOOLS),
    )

    builder.add_edge(START, "assistant")

    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )

    builder.add_edge("tools", "assistant")

    return builder.compile(
        checkpointer=checkpointer,
    )


def build_system_message(
    workspace: str,
    history: str,
    memory: str,
) -> SystemMessage:

    content = f"""
{SYSTEM_PROMPT}

ТЕКУЩАЯ РАБОЧАЯ ДИРЕКТОРИЯ:
{workspace}

ИСТОРИЯ ПРЕДЫДУЩЕГО ДИАЛОГА:
{history}

ДОЛГОСРОЧНАЯ ПАМЯТЬ:
{memory}
"""

    return SystemMessage(content=content)