# Libs
from typing import Any
import json

from fastmcp import Client, ClientGroup
from fastmcp.client.transports import StreamableHttpTransport

from ollama import chat, ChatResponse, Message, Tool

# Application
from core.settings import settings

home_transport = StreamableHttpTransport("http://127.0.0.1:8008/mcp")
home_client = Client(home_transport)

# github_transport = StreamableHttpTransport(
#     "https://api.githubcopilot.com/mcp",
#     headers={
#         "Authorization": f"Bearer {settings.MCP_GITHUB_TOKEN}",
#     },
# )
# github_client = Client(github_transport)

group = ClientGroup(
    {
        "home": home_client,
        # "github": github_client,
    }
)


def _serialize_tool_result(result) -> str:
    if getattr(result, "structured_content", None) is not None:
        return json.dumps(result.structured_content, ensure_ascii=False, default=str)

    text_parts = []

    for block in getattr(result, "content", []) or []:
        if hasattr(block, "text") and block.text:
            text_parts.append(block.text)

    if text_parts:
        return "\n".join(text_parts)

    return json.dumps(
        {
            "success": not getattr(result, "is_error", False),
            "data": str(getattr(result, "data", result)),
        },
        ensure_ascii=False,
        default=str,
    )


def build_ollama_tools(mcp_tools) -> list[Tool]:
    ollama_tools = []

    for tool in mcp_tools:
        schema = (
            getattr(tool, "inputSchema", None)
            or getattr(tool, "input_schema", None)
            or {}
        )

        ollama_tools.append(
            Tool(
                type="function",
                function=Tool.Function(
                    name=tool.name,
                    description=tool.description or "",
                    parameters=schema,
                ),
            )
        )

    return ollama_tools


def _build_messages(history: list[Any]) -> list[Message]:
    messages: list[Message] = []

    for msg in history:
        if isinstance(msg, dict):
            role = msg.get("role")
            content = msg.get("content")
            tool_name = msg.get("tool_name")
        else:
            role = getattr(msg, "role", None)
            content = getattr(msg, "content", None)
            tool_name = getattr(msg, "tool_name", None)

        if hasattr(role, "value"):
            role = role.value

        if role == "assistant" and not (content or "").strip():
            continue

        if role == "tool":
            messages.append(
                Message(
                    role="tool",
                    content=content or "",
                    tool_name=tool_name,
                )
            )
        else:
            messages.append(
                Message(
                    role=role,
                    content=content or "",
                )
            )

    return messages


async def run_agent(history: list[Any]) -> list[Message]:
    messages = _build_messages(history)
    new_messages: list[Message] = []

    async with group:
        mcp_tools = await group.list_tools()
        ollama_tools = build_ollama_tools(mcp_tools)

        response: ChatResponse = chat(
            model=settings.MODEL,
            messages=messages,
            tools=ollama_tools,
        )

        assistant_msg = response.message
        messages.append(assistant_msg)

        if assistant_msg.content and assistant_msg.content.strip():
            new_messages.append(
                Message(
                    role="assistant",
                    content=assistant_msg.content,
                    tool_name=None,
                )
            )

        tool_calls = assistant_msg.tool_calls or []
        if not tool_calls:
            return new_messages

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments or {}

            try:
                result = await group.call_tool(tool_name, arguments)
                tool_content = _serialize_tool_result(result)
            except Exception as exc:
                tool_content = json.dumps(
                    {
                        "success": False,
                        "error": "tool_execution_failed",
                        "message": str(exc),
                    },
                    ensure_ascii=False,
                )

            messages.append(
                Message(
                    role="tool",
                    tool_name=tool_name,
                    content=tool_content,
                )
            )

            new_messages.append(
                Message(
                    role="tool",
                    tool_name=tool_name,
                    content=tool_content,
                )
            )

        final_response: ChatResponse = chat(
            model=settings.MODEL,
            messages=messages,
            tools=ollama_tools,
        )

        final_content = (final_response.message.content or "").strip()

        new_messages.append(
            Message(
                role="assistant",
                content=final_content,
                tool_name=None,
            )
        )

        return new_messages
