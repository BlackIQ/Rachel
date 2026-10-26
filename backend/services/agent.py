# Libs
import json  # JSON
import httpx  # HTTPx

from mcp import Client  # MCP
from mcp.client.streamable_http import streamable_http_client  # MCP HTTP
from mcp_types import TextContent  # MCP Types

from ollama import chat, ChatResponse, Message, Tool  # Ollama

# Application
from core.settings import settings  # Core: Settings

MCP_HOME_URL = "http://127.0.0.1:8080"
MCP_GITHUB_URL = "https://api.githubcopilot.com/mcp"


def _to_ollama_tool(tool) -> Tool:
    return Tool(
        type="function",
        function=Tool.Function(
            name=tool.name,
            description=tool.description or "",
            parameters=tool.input_schema,
        ),
    )


def _serialize_tool_result(result) -> str:
    text_parts = [
        block.text for block in result.content if isinstance(block, TextContent)
    ]

    payload = {
        "success": not result.is_error,
        "content": "\n".join(text_parts),
        "structured_content": getattr(result, "structured_content", None),
    }

    return json.dumps(payload, ensure_ascii=False, default=str)


def _build_messages(history: list[Message]) -> list[Message]:
    messages: list[Message] = []

    for msg in history:
        role = msg["role"]
        content = msg["content"]
        tool_name = msg.get("tool_name")

        if role == "assistant" and not (content or "").strip():
            continue

        if role == "tool":
            messages.append(
                Message(
                    role="tool",
                    content=content,
                    tool_name=tool_name,
                )
            )
        else:
            messages.append(
                Message(
                    role=role,
                    content=content,
                )
            )

    return messages


async def run_agent(history: list[Message]) -> list[Message]:
    messages = _build_messages(history)
    new_messages: list[Message] = []

    headers = {
        "Authorization": f"Bearer {settings.MCP_GITHUB_TOKEN}",
    }

    async with httpx.AsyncClient(headers=headers, timeout=60) as http_client:
        transport = streamable_http_client(
            MCP_SERVER_URL,
            http_client=http_client,
        )

        async with Client(transport) as client:
            tool_list = await client.list_tools()
            available_tools = {tool.name for tool in tool_list.tools}
            tools = [_to_ollama_tool(tool) for tool in tool_list.tools]

            response: ChatResponse = chat(
                model=settings.MODEL,
                messages=messages,
                tools=tools,
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

                if tool_name not in available_tools:
                    tool_content = json.dumps(
                        {
                            "success": False,
                            "error": "tool_not_found",
                            "message": f"Tool {tool_name} not found",
                        },
                        ensure_ascii=False,
                    )
                else:
                    try:
                        result = await client.call_tool(tool_name, arguments)
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
                        content=tool_content,
                        tool_name=tool_name,
                    ),
                )

            final_response: ChatResponse = chat(
                model=settings.MODEL,
                messages=messages,
                tools=tools,
            )

            final_msg = final_response.message
            new_messages.append(
                Message(
                    role="assistant",
                    content=final_msg.content or "",
                    tool_name=None,
                )
            )

            return new_messages
