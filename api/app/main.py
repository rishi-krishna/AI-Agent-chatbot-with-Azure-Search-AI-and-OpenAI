"""
AI Gateway API: retrieval + LLM completion with citations.
"""
import logging

from fastapi import FastAPI, Depends, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import Settings, get_settings
from app.retrieval import search_chunks
from app.chat import chat_with_context


app = FastAPI(
    title="COO Chat AI Gateway",
    description="RAG-backed chat: retrieval (Azure AI Search) + LLM (Azure OpenAI) with citations.",
    version="1.0.0",
)

CORS_ORIGINS = [
    "http://localhost:4200",
    "https://frontend-raraa-drc5acgxa5efc8bs.canadacentral-01.azurewebsites.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.azurewebsites\.net",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class Citation(BaseModel):
    source_file: str
    source_title: str
    content_snippet: str
    relevance_score: float | None = None


class ChatResponse(BaseModel):
    reply: str
    citations: list[Citation]


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, settings: Settings = Depends(get_settings)):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="message is required")
    try:
        chunks = search_chunks(settings, request.message)
    except Exception as e:
        logger.exception("Retrieval failed")
        raise HTTPException(status_code=502, detail=f"Retrieval failed: {e}")
    context = "\n\n---\n\n".join(
        f"[{c['source_file']}] {c['content']}" for c in chunks
    )
    if not context.strip():
        return ChatResponse(
            reply="I couldn't find relevant help content for that. Try rephrasing or use the main menu to explore Approvals, Reports, or Settings.",
            citations=[],
        )
    try:
        reply = chat_with_context(settings, context, request.message)
    except Exception as e:
        logger.exception("LLM failed")
        raise HTTPException(status_code=502, detail=f"LLM failed: {e}")
    snippet_len = settings.citation_snippet_length
    citations = [
        Citation(
            source_file=c["source_file"],
            source_title=c["source_title"],
            content_snippet=(c["content"][:snippet_len] + "..." if len(c["content"]) > snippet_len else c["content"]),
            relevance_score=c.get("relevance_score"),
        )
        for c in chunks
    ]
    return ChatResponse(reply=reply, citations=citations)


@app.get("/health")
def health():
    return {"status": "ok"}
