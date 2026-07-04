import httpx
from app.services.providers.base import LLMProvider


class OllamaProvider(LLMProvider):
    """Ollama LLM Provider (Offline)"""

    def __init__(self, base_url: str, model_name: str):
        self.base_url = base_url
        self.model_name = model_name
        self._resolved_model_name = None

    async def _get_available_models(self) -> list[str]:
        """Return the models currently available in Ollama."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return [model.get("name") for model in data.get("models", []) if model.get("name")]

    async def _resolve_model_name(self) -> str:
        """Choose a model that actually exists in Ollama."""
        if self._resolved_model_name:
            return self._resolved_model_name

        available_models = await self._get_available_models()
        if not available_models:
            self._resolved_model_name = self.model_name
            return self._resolved_model_name

        if self.model_name in available_models:
            self._resolved_model_name = self.model_name
            return self._resolved_model_name

        for candidate in [f"{self.model_name}:latest", self.model_name]:
            if candidate in available_models:
                self._resolved_model_name = candidate
                return self._resolved_model_name

        self._resolved_model_name = available_models[0]
        return self._resolved_model_name

    async def generate(self, prompt: str) -> str:
        """Generate response using Ollama"""
        resolved_model = await self._resolve_model_name()
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": resolved_model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("response", "No response generated")
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                available_models = await self._get_available_models()
                raise RuntimeError(
                    f"Ollama model '{self.model_name}' is unavailable. Installed models: {available_models or 'none'}"
                ) from exc
            raise

    async def health_check(self) -> bool:
        """Check if Ollama is running"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False
