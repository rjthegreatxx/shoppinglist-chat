from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.vector import get_qdrant
from app.config import settings

router = APIRouter()


class ProductDetail(BaseModel):
    product_id: str
    name: str
    description: str


@router.get("/products/{product_id}", response_model=ProductDetail)
async def get_product(product_id: str) -> ProductDetail:
    qdrant = get_qdrant()
    offset = None
    while True:
        results, next_offset = await qdrant.scroll(
            collection_name=settings.qdrant_collection,
            limit=100,
            offset=offset,
            with_payload=True,
        )
        for point in results:
            if point.payload.get("product_id") == product_id:
                return ProductDetail(
                    product_id=point.payload["product_id"],
                    name=point.payload["name"],
                    description=point.payload["description"],
                )
        if next_offset is None:
            break
        offset = next_offset
    raise HTTPException(status_code=404, detail="Product not found")
