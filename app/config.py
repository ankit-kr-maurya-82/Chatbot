from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Provider Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # ollama, openai, gemini
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:latest")

    # Ollama Configuration (Offline)
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Google Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

settings = Settings()