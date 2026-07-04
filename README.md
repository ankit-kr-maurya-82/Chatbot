# LLM Chatbot - Offline Setup Guide

This is a FastAPI-based chatbot using **Ollama** for offline LLM capabilities. No internet connection or API keys required after model download!

## Architecture

```
User (HTTP Request)
   │
   ▼
FastAPI Backend
   │
   ▼
LLM Service Layer
   │
   ▼
Ollama (localhost:11434)
   │
   ▼
Llama 3 / Gemma 3 / Mistral (Local Model)
   │
   ▼
Generated Response
```

## Prerequisites

- Python 3.8+
- Ollama (install from https://ollama.ai)
- 8-16 GB RAM (depending on model)

## Quick Start

### 1. Install Ollama

Download and install from [ollama.ai](https://ollama.ai)

Verify installation:
```bash
ollama --version
```

### 2. Download a Model

Choose one of these models:

**Lightweight (6-8 GB RAM):**
```bash
ollama pull gemma3
# or
ollama pull mistral
```

**Recommended (8-12 GB RAM):**
```bash
ollama pull llama3
```

**High-performance (8-16 GB RAM):**
```bash
ollama pull qwen
```

### 3. Start Ollama

```bash
ollama serve
```

Or run in background:
- **Windows**: Ollama starts automatically after installation
- **Linux/Mac**: `ollama serve` in another terminal

Verify Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

### 4. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Configure Environment

Edit `.env`:
```
OLLAMA_URL=http://localhost:11434
MODEL_NAME=llama3
```

Change `MODEL_NAME` if you installed a different model (e.g., `gemma3`, `mistral`, `qwen`)

### 6. Run the Server

```bash
uvicorn main:app --reload
```

Visit:
- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## API Endpoints

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy"
}
```

### Chat
```bash
POST /chat
Content-Type: application/json

{
  "prompt": "Explain Python decorators"
}
```

Response:
```json
{
  "response": "Python decorators are functions that modify the behavior of another function..."
}
```

## Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is FastAPI?"}'
```

## Project Structure

```
app/
├── api/
│   ├── routes/
│   │   ├── chat.py          # Chat endpoint
│   │   └── health.py        # Health check
│   └── router.py            # Route registration
├── services/
│   └── llm_service.py       # Ollama communication
├── schemas/
│   ├── prompt.py            # Request schema
│   └── response.py          # Response schema
├── exceptions/
│   └── ai_exception.py      # Custom exceptions
├── config.py                # Configuration
└── main.py                  # FastAPI app
.env                         # Environment variables
requirements.txt            # Python dependencies
```

## Model Comparison

| Model | Size | Speed | Quality | RAM |
|-------|------|-------|---------|-----|
| Llama 3 8B | 5.2GB | Medium | Excellent | 8-12GB |
| Gemma 3 | 4.7GB | Fast | Good | 6-8GB |
| Mistral 7B | 4.1GB | Very Fast | Good | 8-10GB |
| Qwen 2.5 | 4.7GB | Fast | Excellent | 8-10GB |
| DeepSeek-R1 | 8GB+ | Slow | Excellent | 12-16GB |

## Troubleshooting

### Ollama connection error
```
Failed to generate AI response: Connection refused
```
**Solution:** Make sure Ollama is running:
```bash
ollama serve
```

### Model not found error
```
Failed to generate AI response: model not found
```
**Solution:** Pull the model first:
```bash
ollama pull llama3
```

### Slow responses
- **Cause:** Using a model too large for your RAM
- **Solution:** Use a smaller model (Gemma 3 or Mistral)

### Out of memory
- **Cause:** Model too large or insufficient RAM
- **Solution:** Use a smaller model or increase system RAM

## Next Steps

- **Phase 3:** Add conversation history
- **Phase 4:** Store chat sessions in database
- **Phase 5:** Stream responses for real-time output
- **Phase 6:** Add RAG with vector databases
- **Phase 7:** Implement tool calling (calculator, file reader, etc.)
- **Phase 8:** Docker deployment

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## License

MIT
