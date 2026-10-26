# Libs
import asyncio  # AsyncIO
import json  # JSON
from typing import Any  # Types
import httpx  # HTTPx

from mcp import Client  # MCP
from mcp.client.streamable_http import streamable_http_client  # MCP HTTP
from mcp_types import TextContent  # MCP Types

from ollama import chat, ChatResponse, Message, Tool  # Ollama

# Application
from core.settings import settings

MCP_SERVERS: list[dict[str, Any]] = [
    {
        "name": "home",
        "url": "http://127.0.0.1:8080/mcp",
        "headers": {},
    },  # Home
    {
        "name": "github",
        "url": "https://api.githubcopilot.com/mcp",
        "headers": {
            "Authorization": f"Bearer {settings.MCP_GITHUB_TOKEN}",
        },
    },  # GitHub
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


async def open_mcp_clients() -> tuple[
    list[tuple[Client, httpx.AsyncClient]],
    dict[str, tuple[Client, str]],
    list[Tool],
]:
    clients: list[tuple[Client, httpx.AsyncClient]] = []
    registry: dict[str, tuple[Client, str]] = {}
    ollama_tools: list[Tool] = []

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

        print(f"[mcp] connected: {server['name']} ({len(tool_list.tools)} tools)")

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

    return clients, registry, ollama_tools


async def close_mcp_clients(clients: list[tuple[Client, httpx.AsyncClient]]) -> None:
    for client, http_client in clients:
        try:
            await client.__aexit__(None, None, None)
        except Exception:
            pass

        try:
            await http_client.aclose()
        except Exception:
            pass


async def process_query(
    query: str,
    messages: list[Message],
    registry: dict[str, tuple[Client, str]],
    ollama_tools: list[Tool],
) -> str:
    messages.append(Message(role="user", content=query))

    response: ChatResponse = chat(
        model=settings.MODEL,
        messages=messages,
        tools=ollama_tools,
    )

    assistant_msg = response.message
    messages.append(assistant_msg)

    tool_calls = assistant_msg.tool_calls or []
    if not tool_calls:
        return assistant_msg.content or ""

    print(f"\n[tools] model requested {len(tool_calls)} tool call(s)")

    for tool_call in tool_calls:
        exposed_name = tool_call.function.name
        arguments = tool_call.function.arguments or {}

        print(f"  -> {exposed_name}({arguments})")

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

        print(f"  <- {tool_content}")

        messages.append(
            Message(
                role="tool",
                tool_name=store_name,
                content=tool_content,
            )
        )

    final_response: ChatResponse = chat(
        model=settings.MODEL,
        messages=messages,
        tools=ollama_tools,
    )

    final_msg = final_response.message
    messages.append(final_msg)

    content = (final_msg.content or "").strip()
    if not content:
        content = "Tool ran, but model returned an empty final answer."

    return content


async def chat_loop() -> None:
    print("Rachel CLI")
    print("Type a message, or 'quit' to exit.\n")

    clients, registry, ollama_tools = await open_mcp_clients()
    messages: list[Message] = []

    try:
        print(f"\n[ready] {len(ollama_tools)} tools available\n")

        while True:
            try:
                query = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nbye")
                break

            if not query:
                continue

            if query.lower() in {"quit", "exit"}:
                print("bye")

                break

            try:
                answer = await process_query(
                    query=query,
                    messages=messages,
                    registry=registry,
                    ollama_tools=ollama_tools,
                )

                print(f"\nRachel: {answer}\n")
            except Exception as exc:
                print(f"\nError: {exc}\n")
    finally:
        await close_mcp_clients(clients)


if __name__ == "__main__":
    asyncio.run(chat_loop())
