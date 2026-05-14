from fastapi import APIRouter

from app.models.schemas import ProductResult, SearchRequest
from app.services.vector import search_products

router = APIRouter()


@router.post("/search", response_model=list[ProductResult])
async def search(request: SearchRequest) -> list[ProductResult]:
    results = await search_products(request.query, top_k=request.top_k)
    return [ProductResult(**r) for r in results]
