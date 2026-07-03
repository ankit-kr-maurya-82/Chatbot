from app.services.providers.base import LLMProvider
from app.services.providers.ollama import OllamaProvider
from app.services.providers.openai_provider import OpenAIProvider
from app.services.providers.gemini import GeminiProvider
from app.config import settings


def get_llm_provider() -> LLMProvider:
    """Factory function to get the configured LLM provider"""

    provider_type = settings.LLM_PROVIDER.lower()

    if provider_type == "ollama":
        return OllamaProvider(
            base_url=settings.OLLAMA_URL,
            model_name=settings.MODEL_NAME
        )

    elif provider_type == "openai":
        return OpenAIProvider(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.MODEL_NAME
        )

    elif provider_type == "gemini":
        return GeminiProvider(
            api_key=settings.GEMINI_API_KEY,
            model_name=settings.MODEL_NAME
        )

    else:
        raise ValueError(f"Unknown LLM provider: {provider_type}")
