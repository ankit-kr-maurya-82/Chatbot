from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a response from the LLM"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is available"""
        pass
