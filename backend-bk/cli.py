# Libs
import asyncio  # Asyncio
import json  # JSON

from fastmcp import Client, ClientGroup  # FastMCP Client
from fastmcp.client.transports import StreamableHttpTransport  # FastMCP Transports

from ollama import chat, ChatResponse, Message, Tool  # Ollama

# Application
from core.settings import settings  # Core: Settings

rachel_transport = StreamableHttpTransport("http://127.0.0.1:8008/mcp")
rachel_client = Client(rachel_transport)

group = ClientGroup(
    {
        "rachel": rachel_client,
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
        ollama_tools.append(
            Tool(
                type="function",
                function=Tool.Function(
                    name=tool.name,
                    description=tool.description or "",
                ),
            )
        )

    return ollama_tools


async def process_query(
    query: str,
    messages: list[Message],
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
        tool_name = tool_call.function.name
        arguments = tool_call.function.arguments or {}

        print(f"  -> {tool_name}({arguments})")

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

        print(f"  <- {tool_content[:300]}{'...' if len(tool_content) > 300 else ''}")

        messages.append(
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

    final_msg = final_response.message
    messages.append(final_msg)

    content = (final_msg.content or "").strip()
    if not content:
        content = "Tool ran, but model returned an empty final answer."

    return content


async def chat_loop(ollama_tools: list[Tool]) -> None:
    print("Rachel CLI")
    print("Type a message, or 'quit' to exit.\n")
    print(f"[ready] {len(ollama_tools)} tools available\n")

    messages: list[Message] = []

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
                ollama_tools=ollama_tools,
            )

            print(f"\nRachel: {answer}\n")
        except Exception as exc:
            print(f"\nError: {exc}\n")


async def main() -> None:
    async with group:
        mcp_tools = await group.list_tools()
        ollama_tools = build_ollama_tools(mcp_tools)

        await chat_loop(ollama_tools)


if __name__ == "__main__":
    asyncio.run(main())
