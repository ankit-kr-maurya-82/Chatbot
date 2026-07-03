import google.generativeai as genai
from app.services.providers.base import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini LLM Provider"""

    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(self.model_name)

    async def generate(self, prompt: str) -> str:
        """Generate response using Google Gemini"""
        response = self.model.generate_content(prompt)
        return response.text

    async def health_check(self) -> bool:
        """Check if Gemini API is accessible"""
        try:
            self.model.generate_content("test")
            return True
        except Exception:
            return False
