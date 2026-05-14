from fastapi import APIRouter, Path
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest
from app.services.llm import stream_chat

router = APIRouter()


@router.post("/chat/{session_id}")
async def chat(
    session_id: str = Path(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$"),
    request: ChatRequest = ...,
) -> StreamingResponse:
    return StreamingResponse(
        stream_chat(session_id, request.message),
        media_type="text/plain",
    )
