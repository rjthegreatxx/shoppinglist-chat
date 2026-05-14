import logging

from qdrant_client import AsyncQdrantClient

from app.config import settings

logger = logging.getLogger(__name__)

_qdrant: AsyncQdrantClient | None = None


def init_qdrant() -> None:
    global _qdrant
    if not settings.qdrant_configured:
        raise RuntimeError("Qdrant is not configured — set QDRANT_URL and QDRANT_API_KEY")
    _qdrant = AsyncQdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )
    logger.info("Qdrant client initialised url=%s", settings.qdrant_url)


def get_qdrant() -> AsyncQdrantClient:
    assert _qdrant is not None, "Qdrant not initialised — call init_qdrant() at startup"
    return _qdrant


async def search_products(query: str, top_k: int | None = None) -> list[dict]:
    from app.services.llm import get_openai_client

    k = top_k if top_k is not None else settings.rag_top_k

    try:
        embedding_resp = await get_openai_client().embeddings.create(
            model=settings.embedding_model,
            input=query,
        )
        vector = embedding_resp.data[0].embedding

        response = await get_qdrant().query_points(
            collection_name=settings.qdrant_collection,
            query=vector,
            limit=k,
            score_threshold=settings.rag_score_threshold,
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

        logger.info(
            "Vector search query=%r returned %d results (threshold=%.2f)",
            query, len(products), settings.rag_score_threshold,
        )
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
