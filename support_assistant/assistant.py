import os
from typing import TypedDict

from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END

from retrieve import retrieve_documents


MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"


class AssistantResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)


class AssistantState(TypedDict):
    question: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float


def classify_intent(state: AssistantState):
    question = state["question"].lower()

    policy_keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours",
    ]

    if MOCK_LLM:
        if any(keyword in question for keyword in policy_keywords):
            intent = "policy_question"
        else:
            intent = "general_question"

        return {
            "intent": intent
        }

    raise NotImplementedError(
        "Real LLM intent classification is optional and not enabled yet."
    )


def retrieve_and_answer(state: AssistantState):
    question = state["question"]

    retrieved = retrieve_documents(
        question,
        top_k=3
    )

    if not retrieved:
        response = AssistantResponse(
            answer="I could not find relevant information in the Zepto policy documents.",
            sources=[],
            confidence=0.0,
        )

        return {
            "answer": response.answer,
            "sources": response.sources,
            "confidence": response.confidence,
        }

    top_chunk = retrieved[0]

    if MOCK_LLM:
        snippet = top_chunk["document"][:200]

        answer = f"Based on the retrieved context: {snippet}"

        sources = [
            result["source"]
            for result in retrieved
        ]

        response = AssistantResponse(
            answer=answer,
            sources=sources,
            confidence=1.0,
        )

        return {
            "answer": response.answer,
            "sources": response.sources,
            "confidence": response.confidence,
        }

    raise NotImplementedError(
        "Real LLM answer generation is optional and not enabled yet."
    )


def direct_answer(state: AssistantState):
    if MOCK_LLM:
        response = AssistantResponse(
            answer="I can only answer questions about Zepto policies right now.",
            sources=[],
            confidence=1.0,
        )

        return {
            "answer": response.answer,
            "sources": response.sources,
            "confidence": response.confidence,
        }

    raise NotImplementedError(
        "Real LLM direct answering is optional and not enabled yet."
    )


def route_question(state: AssistantState):
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


workflow = StateGraph(AssistantState)

workflow.add_node(
    "classify_intent",
    classify_intent
)

workflow.add_node(
    "retrieve_and_answer",
    retrieve_and_answer
)

workflow.add_node(
    "direct_answer",
    direct_answer
)

workflow.set_entry_point("classify_intent")

workflow.add_conditional_edges(
    "classify_intent",
    route_question,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer",
    },
)

workflow.add_edge(
    "retrieve_and_answer",
    END
)

workflow.add_edge(
    "direct_answer",
    END
)

app = workflow.compile()


if __name__ == "__main__":

    policy_question = (
        "How long do I have to report a damaged or missing item after delivery?"
    )

    policy_result = app.invoke(
        {
            "question": policy_question,
            "intent": "",
            "answer": "",
            "sources": [],
            "confidence": 0.0,
        }
    )

    print("\nPOLICY QUESTION")
    print("Question:", policy_question)
    print("Intent:", policy_result["intent"])
    print("Answer:", policy_result["answer"])
    print("Sources:", policy_result["sources"])
    print("Confidence:", policy_result["confidence"])

    general_question = "What is the capital of France?"

    general_result = app.invoke(
        {
            "question": general_question,
            "intent": "",
            "answer": "",
            "sources": [],
            "confidence": 0.0,
        }
    )

    print("\nGENERAL QUESTION")
    print("Question:", general_question)
    print("Intent:", general_result["intent"])
    print("Answer:", general_result["answer"])
    print("Sources:", general_result["sources"])
    print("Confidence:", general_result["confidence"])


 # Structured prompt required for the optional real-LLM path.
STRUCTURED_PROMPT = """
Role:
You are a Zepto customer support policy assistant.

Context:
Use only the retrieved Zepto policy context provided below.

Task:
Answer the user's question using the retrieved policy context.

Format:
Return a concise, direct answer and identify the source documents used.

Length:
Keep the answer short and relevant.

Negative constraint:
Do not invent, assume, or use information that is not present in the retrieved policy context.

Few-shot example:
Question: How long do I have to report a damaged or missing item after delivery?
Context: A damaged or missing item should be reported according to the applicable Zepto policy.
Answer: Based on the retrieved context, follow the applicable Zepto policy for reporting the damaged or missing item.

Retrieved context:
{context}

User question:
{question}
"""


def call_with_retry(llm_function, max_retries=3):
    """
    Retry an optional real-LLM call when it fails.
    The default MOCK_LLM path does not use this function.
    """
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            return llm_function()
        except Exception as error:
            last_error = error

    raise RuntimeError(
        f"Real LLM call failed after {max_retries} attempts: {last_error}"
    )   