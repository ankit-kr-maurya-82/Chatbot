from fastapi import APIRouter

from app.services.llm_service import clear_chat_history, get_chat_history

router = APIRouter()

@router.get("/history")
async def history():
    return {"history": await get_chat_history()}

@router.delete("/history")
async def clear_history():
    await clear_chat_history()
    return {"status": "success", "message": "Chat history cleared."}
