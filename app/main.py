from fastapi import FastAPI
from app.api.router import router


app = FastAPI(
    title="LLM Chatbot",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "LLM Chatbot API"
    }

app.include_router(router)