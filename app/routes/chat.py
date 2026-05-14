from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest
from app.services.llm import stream_chat

router = APIRouter()


@router.post("/chat/{session_id}")
async def chat(session_id: str, request: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        stream_chat(session_id, request.message),
        media_type="text/plain",
    )
