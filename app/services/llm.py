import logging
from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.config import settings
from app.services.history import get_history, save_message

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=settings.do_inference_api_key,
    base_url=settings.do_inference_base_url,
)

SYSTEM_PROMPT = "You are a helpful assistant."


async def stream_chat(session_id: str, user_message: str) -> AsyncIterator[str]:
    history = await get_history(session_id)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
        {"role": "user", "content": user_message}
    ]

    logger.info("Chat request session=%s model=%s history_len=%d", session_id, settings.do_model, len(history))

    full_response: list[str] = []
    stream_started = False

    try:
        stream = await client.chat.completions.create(
            model=settings.do_model,
            messages=messages,
            stream=True,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                if not stream_started:
                    stream_started = True
                    await save_message(session_id, "user", user_message)
                full_response.append(delta)
                yield delta

        if stream_started:
            await save_message(session_id, "assistant", "".join(full_response))
            logger.info("Chat complete session=%s response_len=%d", session_id, len("".join(full_response)))
        else:
            logger.warning("Empty response from LLM session=%s", session_id)

    except Exception:
        logger.exception("LLM stream error session=%s", session_id)
        if full_response:
            await save_message(session_id, "assistant", "".join(full_response))
        yield "\n\n[Error: the response was interrupted. Please try again.]"
