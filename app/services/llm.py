import json
import logging
from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.config import settings
from app.services.history import get_history, save_message

logger = logging.getLogger(__name__)

_client: AsyncOpenAI | None = None


def init_openai() -> None:
    global _client
    _client = AsyncOpenAI(
        api_key=settings.do_inference_api_key,
        base_url=settings.do_inference_base_url,
    )
    logger.info("OpenAI client initialised base_url=%s", settings.do_inference_base_url)


def get_openai_client() -> AsyncOpenAI:
    assert _client is not None, "OpenAI client not initialised — call init_openai() at startup"
    return _client


SYSTEM_PROMPT = (
    "You are a helpful medical supply assistant. "
    "You ONLY recommend products from the catalog provided in the context. "
    "NEVER invent, hallucinate, or reference products not explicitly listed in the context. "
    "If no relevant products are found in the context, say so honestly rather than suggesting products from memory. "
    "Always cite the exact product name and ID from the catalog when making recommendations."
)

_RAG_SKIP_THRESHOLD = 3


def _should_skip_rag(message: str) -> bool:
    """Skip vector search for very short conversational messages (greetings, acks, etc.)."""
    return len(message.split()) < _RAG_SKIP_THRESHOLD


async def stream_chat(session_id: str, user_message: str) -> AsyncIterator[str]:
    from app.services.vector import format_context, search_products

    history = await get_history(session_id)

    if _should_skip_rag(user_message):
        products = []
        logger.info("RAG skipped for short message session=%s", session_id)
    else:
        products = await search_products(user_message)

    context = format_context(products)
    user_content = f"{context}\n\nUSER REQUEST: {user_message}" if context else user_message

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
        {"role": "user", "content": user_content}
    ]

    logger.info(
        "Chat request session=%s model=%s history_len=%d rag_results=%d",
        session_id, settings.do_model, len(history), len(products),
    )

    if products:
        sources = [{"id": p["product_id"], "name": p["name"]} for p in products]
        yield "__SOURCES__:" + json.dumps({"sources": sources}) + "\n"

    full_response: list[str] = []
    stream_started = False

    try:
        stream = await get_openai_client().chat.completions.create(
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
            response_text = "".join(full_response)
            await save_message(session_id, "assistant", response_text)
            logger.info("Chat complete session=%s response_len=%d", session_id, len(response_text))
        else:
            logger.warning("Empty response from LLM session=%s", session_id)

    except Exception:
        logger.exception("LLM stream error session=%s", session_id)
        if full_response:
            await save_message(session_id, "assistant", "".join(full_response))
        yield "\n\n[Error: the response was interrupted. Please try again.]"
