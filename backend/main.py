
import os
import json
from pathlib import Path
from pydantic import field_validator
from diagnostics import log_failure, public_error

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from google import genai

load_dotenv(Path(__file__).resolve().with_name(".env"))

app = FastAPI(title="AI Streaming Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


    @field_validator("message")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("Message must not be blank")
        return value.strip()


@app.get("/")
def home():
    return {"message": "AI Streaming API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat/stream")
def stream_chat(request: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or not api_key.strip():
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is not configured"
        )

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    def generate():
        try:
            with genai.Client(api_key=api_key) as client:
                response = client.models.generate_content_stream(
                    model=model, contents=request.message,
                )
                received = False
                for chunk in response:
                    if chunk.text:
                        received = True
                        yield sse({"type": "chunk", "text": chunk.text})
                if not received:
                    raise RuntimeError("Gemini returned no text")
            yield sse({"type": "done"})
        except Exception as exc:
            log_failure(exc)
            yield sse({"type": "error", **public_error(exc)})

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


def sse(data):
    return f"data: {json.dumps(data)}\n\n"
