import os
from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.services.history import get_history, save_message

client = AsyncOpenAI(
    api_key=os.getenv("DO_INFERENCE_API_KEY"),
    base_url=os.getenv("DO_INFERENCE_BASE_URL", "https://inference.do-ai.run/v1"),
)

MODEL = os.getenv("DO_MODEL", "llama3.3-instruct-70b")

SYSTEM_PROMPT = "You are a helpful assistant."


async def stream_chat(session_id: str, user_message: str) -> AsyncIterator[str]:
    history = get_history(session_id)
    save_message(session_id, "user", user_message)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
        {"role": "user", "content": user_message}
    ]

    full_response = []

    async with client.chat.completions.stream(
        model=MODEL,
        messages=messages,
    ) as stream:
        async for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                full_response.append(delta)
                yield delta

    save_message(session_id, "assistant", "".join(full_response))
