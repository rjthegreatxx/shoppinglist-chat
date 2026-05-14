from fastapi import APIRouter, Path
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest
from app.services.history import get_history
from app.services.llm import stream_chat

router = APIRouter()

SESSION_ID_PATH = Path(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")


@router.get("/history/{session_id}")
async def history(session_id: str = SESSION_ID_PATH) -> list[dict]:
    return await get_history(session_id)


@router.post("/chat/{session_id}")
async def chat(
    session_id: str = SESSION_ID_PATH,
    request: ChatRequest = ...,
) -> StreamingResponse:
    return StreamingResponse(
        stream_chat(session_id, request.message),
        media_type="text/plain",
    )
