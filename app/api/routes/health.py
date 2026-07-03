from fastapi import APIRouter
from app.services.llm_service import health_check
from app.config import settings

router = APIRouter()

@router.get("/health")
async def health():
    """Health check endpoint with LLM provider status"""
    llm_available = await health_check()
    
    return {
        "status": "healthy",
        "llm_provider": settings.LLM_PROVIDER,
        "model": settings.MODEL_NAME,
        "llm_available": llm_available
    }