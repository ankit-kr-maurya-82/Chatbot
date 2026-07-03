from fastapi import APIRouter, HTTPException

from app.schemas.prompt import Prompt
from app.schemas.response import ChatResponse
from app.services.llm_service import generate_response
from app.exceptions.ai_exception import AIServiceError

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(data: Prompt):

    try:
        reply = await generate_response(data.prompt)

        return ChatResponse(
            response=reply
        )

    except AIServiceError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )