import logging

from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient

from app.config import settings

logger = logging.getLogger(__name__)

COLLECTION = "products"
EMBEDDING_MODEL = "all-mini-lm-l6-v2"

_openai: AsyncOpenAI | None = None
_qdrant: AsyncQdrantClient | None = None


def get_openai() -> AsyncOpenAI:
    global _openai
    if _openai is None:
        _openai = AsyncOpenAI(
            api_key=settings.do_inference_api_key,
            base_url=settings.do_inference_base_url,
        )
    return _openai


def get_qdrant() -> AsyncQdrantClient:
    global _qdrant
    if _qdrant is None:
        _qdrant = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
    return _qdrant


async def search_products(query: str, top_k: int = 5) -> list[dict]:
    try:
        embedding_resp = await get_openai().embeddings.create(
            model=EMBEDDING_MODEL,
            input=query,
        )
        vector = embedding_resp.data[0].embedding

        response = await get_qdrant().query_points(
            collection_name=COLLECTION,
            query=vector,
            limit=top_k,
        )

        products = [
            {
                "product_id": r.payload.get("product_id"),
                "name": r.payload.get("name"),
                "description": r.payload.get("description"),
                "score": round(r.score, 3),
            }
            for r in response.points
        ]

        logger.info("Vector search query=%r returned %d results", query, len(products))
        return products

    except Exception:
        logger.exception("Vector search failed for query=%r", query)
        return []


def format_context(products: list[dict]) -> str:
    if not products:
        return ""
    lines = ["RELEVANT PRODUCTS FROM CATALOG:"]
    for i, p in enumerate(products, 1):
        lines.append(f"{i}. {p['name']} (ID: {p['product_id']})")
        lines.append(f"   {p['description']}")
    return "\n".join(lines)
