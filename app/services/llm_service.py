from app.services.providers.factory import get_llm_provider
from app.exceptions.ai_exception import AIServiceError
from app.services.chat_history import chat_history

# Initialize provider on module load
_provider = None

def _get_provider():
    global _provider
    if _provider is None:
        _provider = get_llm_provider()
    return _provider

async def generate_response(prompt: str) -> str:
    """Generate response using the configured LLM provider"""
    try:
        chat_history.add_message("user", prompt)
        provider = _get_provider()
        response = await provider.generate(prompt)
        chat_history.add_message("assistant", response)
        return response
    except Exception as exc:
        raise AIServiceError(f"Failed to generate AI response: {str(exc)}") from exc

async def health_check() -> bool:
    """Check if the LLM provider is available"""
    try:
        provider = _get_provider()
        return await provider.health_check()
    except Exception:
        return False

async def get_chat_history() -> list:
    """Return stored chat history."""
    return chat_history.get_history()

async def clear_chat_history() -> None:
    """Clear stored chat history."""
    chat_history.clear()
