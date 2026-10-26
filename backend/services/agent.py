# Libs
from typing import Any  # Types
import json  # JSON
import httpx  # HTTPx

from mcp import Client  # MCP
from mcp.client.streamable_http import streamable_http_client  # MCP HTTP
from mcp_types import TextContent  # MCP Types

from ollama import chat, ChatResponse, Message, Tool  # Ollama

# Application
from core.settings import settings  # Core: Settings

MCP_SERVERS: list[dict[str, Any]] = [
    {
        "name": "home",
        "url": "http://127.0.0.1:8080",
        "headers": {},
    },
    {
        "name": "github",
        "url": "https://api.githubcopilot.com/mcp/",
        "headers": {
            "Authorization": f"Bearer {settings.MCP_GITHUB_TOKEN}",
        },
    },
]


def _serialize_tool_result(result) -> str:
    structured = getattr(result, "structured_content", None)

    if structured is not None:
        return json.dumps(structured, ensure_ascii=False, default=str)

    text_parts = [
        block.text for block in result.content if isinstance(block, TextContent)
    ]

    if text_parts:
        return "\n".join(text_parts)

    return json.dumps(
        {
            "success": not result.is_error,
            "content": str(result.content),
        },
        ensure_ascii=False,
        default=str,
    )


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

    clients: list[tuple[Client, httpx.AsyncClient]] = []
    registry: dict[str, tuple[Client, str]] = {}
    ollama_tools: list[Tool] = []

    try:
        for server in MCP_SERVERS:
            http_client = httpx.AsyncClient(
                headers=server.get("headers") or {},
                timeout=60.0,
            )
            transport = streamable_http_client(
                server["url"],
                http_client=http_client,
            )

            client = Client(transport)

            await client.__aenter__()

            clients.append((client, http_client))

            tool_list = await client.list_tools()
            for tool in tool_list.tools:
                exposed_name = f"{server['name']}__{tool.name}"
                registry[exposed_name] = (client, tool.name)

                ollama_tools.append(
                    Tool(
                        type="function",
                        function=Tool.Function(
                            name=exposed_name,
                            description=f"[{server['name']}] {tool.description or ''}",
                            parameters=tool.input_schema,
                        ),
                    )
                )

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
                ),
            )

        tool_calls = assistant_msg.tool_calls or []
        if not tool_calls:
            return new_messages

        for tool_call in tool_calls:
            exposed_name = tool_call.function.name
            arguments = tool_call.function.arguments or {}

            if exposed_name not in registry:
                tool_content = json.dumps(
                    {
                        "success": False,
                        "error": "tool_not_found",
                        "message": f"Tool {exposed_name} not found",
                    },
                    ensure_ascii=False,
                )
                store_name = exposed_name
            else:
                client, real_name = registry[exposed_name]
                store_name = exposed_name
                try:
                    result = await client.call_tool(real_name, arguments)
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
                    tool_name=store_name,
                    content=tool_content,
                )
            )
            new_messages.append(
                Message(
                    role="tool",
                    tool_name=tool_content,
                    content=store_name,
                ),
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
            ),
        )

        return new_messages

    finally:
        for client, http_client in clients:
            try:
                await client.__aexit__(None, None, None)
            except Exception:
                pass

            try:
                await http_client.aclose()
            except Exception:
                pass
