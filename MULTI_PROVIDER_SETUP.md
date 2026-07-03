# Multi-Provider LLM Chatbot

This FastAPI chatbot supports multiple LLM providers, allowing you to choose between offline and cloud-based options.

## Supported Providers

| Provider | Type | Setup | Cost |
|----------|------|-------|------|
| **Ollama** | Offline | Download model locally | Free |
| **OpenAI** | Cloud | API key required | $0.01-0.03/1K tokens |
| **Google Gemini** | Cloud | API key required | Free tier available |

## Quick Switch Guide

### 1. Using Ollama (Default - Offline)

**Setup:**
```bash
# Install Ollama from https://ollama.ai
ollama serve
ollama pull llama3
```

**.env:**
```
LLM_PROVIDER=ollama
MODEL_NAME=llama3
OLLAMA_URL=http://localhost:11434
```

**Test:**
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"prompt":"Hello"}'
```

---

### 2. Using OpenAI (Cloud)

**Setup:**
1. Get API key from [platform.openai.com](https://platform.openai.com)

**.env:**
```
LLM_PROVIDER=openai
MODEL_NAME=gpt-4
OPENAI_API_KEY=sk-your-api-key-here
```

**Supported Models:**
- `gpt-4` - Most capable
- `gpt-4-turbo` - Fast & capable
- `gpt-3.5-turbo` - Budget-friendly

---

### 3. Using Google Gemini (Cloud)

**Setup:**
1. Get API key from [ai.google.dev](https://ai.google.dev)

**.env:**
```
LLM_PROVIDER=gemini
MODEL_NAME=gemini-pro
GEMINI_API_KEY=your-gemini-api-key
```

**Supported Models:**
- `gemini-pro` - General purpose
- `gemini-pro-vision` - With image understanding

---

## Architecture

```
User Request (POST /chat)
       │
       ▼
Chat Route (validates input)
       │
       ▼
LLM Service (provider agnostic)
       │
       ▼
Provider Factory
       │
    ┌──┼──┬──────────┐
    │  │  │          │
    ▼  ▼  ▼          ▼
Ollama OpenAI Gemini Custom...
```

## Project Structure

```
app/
├── services/
│   ├── providers/
│   │   ├── base.py           # Abstract base class
│   │   ├── ollama.py         # Ollama implementation
│   │   ├── openai_provider.py # OpenAI implementation
│   │   ├── gemini.py         # Google Gemini implementation
│   │   ├── factory.py        # Provider factory
│   │   └── __init__.py
│   ├── llm_service.py        # High-level LLM interface
│   └── ...
├── config.py                 # Configuration loader
└── ...
```

## Code Examples

### Adding a New Provider

1. **Create provider class:**
```python
# app/services/providers/huggingface.py
from app.services.providers.base import LLMProvider

class HuggingFaceProvider(LLMProvider):
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name

    async def generate(self, prompt: str) -> str:
        # Your implementation here
        pass

    async def health_check(self) -> bool:
        # Your health check here
        pass
```

2. **Update factory:**
```python
# In factory.py
elif provider_type == "huggingface":
    return HuggingFaceProvider(
        api_key=settings.HF_API_KEY,
        model_name=settings.MODEL_NAME
    )
```

3. **Update config:**
```python
# In config.py
HF_API_KEY = os.getenv("HF_API_KEY", "")
```

### Using in Code

```python
from app.services.llm_service import generate_response

response = await generate_response("Explain FastAPI")
```

The provider is handled automatically based on `.env` configuration.

## API Endpoints

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "llm_provider": "ollama",
  "model": "llama3",
  "llm_available": true
}
```

### Chat
```bash
POST /chat
Content-Type: application/json

{
  "prompt": "What is machine learning?"
}
```

Response:
```json
{
  "response": "Machine learning is a subset of AI that enables systems to learn from data..."
}
```

## Costs Comparison

### Ollama (Offline)
- **Cost:** Free
- **Speed:** Depends on local hardware
- **Privacy:** 100% local, no data sent
- **Internet:** Not required after model download

### OpenAI GPT-4
- **Cost:** $0.03 input / $0.06 output per 1K tokens
- **Speed:** Very fast
- **Privacy:** Sent to OpenAI servers
- **Internet:** Required

### Google Gemini
- **Cost:** Free tier available, then $0.0001-0.0004 per 1K tokens
- **Speed:** Fast
- **Privacy:** Sent to Google servers
- **Internet:** Required

## Troubleshooting

### "Failed to generate AI response"

**Ollama:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags
ollama serve  # Start if not running
```

**OpenAI:**
```bash
# Verify API key in .env
# Check API key validity at platform.openai.com
```

**Gemini:**
```bash
# Verify API key in .env
# Check API key validity at ai.google.dev
```

### Provider not recognized
```
ValueError: Unknown LLM provider: xyz
```

Check `.env` - `LLM_PROVIDER` must be `ollama`, `openai`, or `gemini`.

### Model not found
```
Provider-specific error about model not found
```

**Ollama:** Run `ollama pull model_name`
**OpenAI:** Verify model name is correct (e.g., `gpt-4`)
**Gemini:** Use `gemini-pro` or `gemini-pro-vision`

## Performance Tips

- **Ollama:** Use smaller models for faster responses (Gemma 3, Mistral)
- **OpenAI:** Use `gpt-3.5-turbo` for faster/cheaper responses
- **Gemini:** Free tier is limited, use for testing/development

## Next Steps

- Add conversation history
- Implement streaming responses
- Add tool calling
- Deploy with Docker
- Add authentication

## Resources

- [Ollama Docs](https://github.com/ollama/ollama)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Google Gemini Docs](https://ai.google.dev/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
