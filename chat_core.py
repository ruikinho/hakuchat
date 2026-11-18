import os

from openai import OpenAI

from search import web_search

MODEL = "nvidia/nemotron-3.5-super-vl:free"
BASE_URL = "https://openrouter.ai/api/v1"


def _get_client() -> OpenAI:
    api_key = os.environ["OPENROUTER_API_KEY"]
    return OpenAI(base_url=BASE_URL, api_key=api_key)


WEB_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for information about a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query, e.g. Helsinki",
                },
            },
            "required": ["query"],
        },
    },
}


def _run_tool_call(tool_call) -> str:
    name = tool_call.function.name
    arguments = tool_call.function.arguments
    import json

    args = json.loads(arguments) if isinstance(arguments, str) else arguments

    if name == "web_search":
        return web_search(args["query"])
    raise ValueError(f"Unknown tool: {name}")


def ask_chat(messages: list[dict]) -> tuple[str, list[str]]:
    client = _get_client()
    tools = [WEB_SEARCH_TOOL]
    searches_used: list[str] = []

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    message = response.choices[0].message
    tool_calls = message.tool_calls or []

    if not tool_calls:
        return message.content or "", searches_used

    search_results = []
    for tool_call in tool_calls:
        result = _run_tool_call(tool_call)
        searches_used.append(tool_call.function.name)
        search_results.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_call.function.name,
                "content": result,
            }
        )

    follow_up = client.chat.completions.create(
        model=MODEL,
        messages=[
            *messages,
            message,
            *search_results,
        ],
        tools=tools,
        tool_choice="none",
    )

    final_content = follow_up.choices[0].message.content or ""
    return final_content, searches_used
