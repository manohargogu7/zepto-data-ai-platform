from fastapi import FastAPI
from pydantic import BaseModel

from assistant import app as assistant_app


api = FastAPI(
    title="Zepto Support Assistant",
    description="RAG-based Zepto policy support assistant",
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str


@api.post("/ask")
def ask_question(request: AskRequest):
    result = assistant_app.invoke(
        {
            "question": request.question,
            "intent": "",
            "response": "",
        }
    )

    return {
        "answer": result["answer"],
        "sources": result.get("sources", []),
        "confidence": result.get("confidence", 0.0),
    }


@api.get("/")
def root():
    return {
        "message": "Zepto Support Assistant API is running"
    }