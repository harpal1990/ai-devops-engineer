import asyncio
import json
import os
import sys

import ollama

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


MODEL = "qwen3:4b"


async def main():

    print("=" * 60)
    print(" AI DEVOPS ENGINEER")
    print("=" * 60)
    print(f"Model: {MODEL}")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server/server.py"],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools_result = await session.list_tools()

            print("\nAvailable MCP tools:")

            for tool in tools_result.tools:
                print(f"  ✓ {tool.name}")

            # Convert MCP tools to Ollama tool format
            ollama_tools = []

            for tool in tools_result.tools:

                ollama_tools.append(
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.input_schema,
                        },
                    }
                )

            print("\n" + "=" * 60)
            print(" AI DEVOPS ENGINEER READY")
            print("=" * 60)

            user_prompt = input("\nYou: ")

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an AI DevOps Engineer. "
                        "Use the available tools to inspect the server "
                        "and provide accurate technical analysis. "
                        "Never invent monitoring data. "
                        "Use tools whenever real system information "
                        "is required."
                    ),
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ]

            response = ollama.chat(
                model=MODEL,
                messages=messages,
                tools=ollama_tools,
            )

            message = response["message"]

            # Display tool calls requested by the AI
            if message.get("tool_calls"):

                print("\nAI requested the following tools:")

                for call in message["tool_calls"]:

                    function_name = call["function"]["name"]

                    arguments = call["function"].get(
                        "arguments",
                        {},
                    )

                    print(
                        f"\n  → {function_name}"
                    )

                    print(
                        f"    Arguments: {arguments}"
                    )

            else:

                print("\nAI did not request any tools.")

            # Process tool calls
            if message.get("tool_calls"):

                messages.append(message)

                for call in message["tool_calls"]:

                    function_name = call["function"]["name"]

                    arguments = call["function"].get(
                        "arguments",
                        {},
                    )

                    print(
                        f"\nExecuting MCP tool: {function_name}"
                    )

                    result = await session.call_tool(
                        function_name,
                        arguments,
                    )

                    tool_output = result.content

                    print(
                        f"Tool result received: {function_name}"
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": function_name,
                            "content": json.dumps(
                                [
                                    item.model_dump()
                                    if hasattr(item, "model_dump")
                                    else str(item)
                                    for item in tool_output
                                ]
                            ),
                        }
                    )

                # Ask Qwen3 to analyze the collected information
                final_response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                )

                print("\n" + "=" * 60)
                print(" DEVOPS ANALYSIS")
                print("=" * 60)

                print(
                    final_response["message"]["content"]
                )

            else:

                print("\n" + "=" * 60)
                print(" AI RESPONSE")
                print("=" * 60)

                print(message["content"])


if __name__ == "__main__":
    asyncio.run(main())