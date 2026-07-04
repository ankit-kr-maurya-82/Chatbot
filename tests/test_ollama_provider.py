import asyncio
import unittest
from unittest.mock import patch

from app.services.providers.ollama import OllamaProvider


class FakeResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


class OllamaProviderTests(unittest.TestCase):
    def test_resolve_model_name_falls_back_to_first_available_model(self):
        provider = OllamaProvider("http://localhost:11434", "llama3")

        async def run_test():
            with patch("app.services.providers.ollama.httpx.AsyncClient") as mock_client:
                mock_client.return_value.__aenter__.return_value.get.return_value = FakeResponse(
                    200,
                    {"models": [{"name": "llama3.2:latest"}]},
                )
                return await provider._resolve_model_name()

        resolved = asyncio.run(run_test())
        self.assertEqual(resolved, "llama3.2:latest")


if __name__ == "__main__":
    unittest.main()
