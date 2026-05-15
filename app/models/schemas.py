from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(default=10, ge=1, le=50)


class ProductResult(BaseModel):
    product_id: str
    name: str
    description: str
    score: float


class CheckoutItem(BaseModel):
    product_id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., ge=1, le=100)


class CheckoutRequest(BaseModel):
    items: list[CheckoutItem] = Field(..., min_length=1)


class CheckoutResponse(BaseModel):
    url: str
