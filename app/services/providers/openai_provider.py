from openai import OpenAI
from app.services.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI LLM Provider"""

    def __init__(self, api_key: str, model_name: str):
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    async def generate(self, prompt: str) -> str:
        """Generate response using OpenAI"""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content

    async def health_check(self) -> bool:
        """Check if OpenAI API is accessible"""
        try:
            self.client.models.list()
            return True
        except Exception:
            return False
