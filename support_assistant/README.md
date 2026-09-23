# Zepto Support Assistant

## Overview

This module implements a Retrieval-Augmented Generation (RAG) based support assistant for Zepto policy questions.

The assistant uses 8 local Zepto policy documents as its knowledge base. The documents are embedded using the `all-MiniLM-L6-v2` Sentence Transformers model and stored in a local ChromaDB vector database.

A LangGraph workflow classifies each question and routes it either to policy retrieval or to a direct canned response. FastAPI provides the `/ask` API.

The required graded path uses deterministic mock mode by default through the `MOCK_LLM` environment variable. No paid service or LLM API key is required.

---

## Project Structure

```text
support_assistant/
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
├── chroma_db/
├── ingest.py
├── retrieve.py
├── assistant.py
├── main.py
├── Dockerfile
└── README.md

chroma_db/ is generated locally and is excluded from Git tracking.

Knowledge Base

The assistant uses 8 policy documents covering topics including:

Delivery and serviceable locations
Returns and refunds
Order cancellation
Damaged or missing items
Payments and wallet-related policies
Membership-related policies
Gift cards
Customer support hours

All 8 documents are loaded and embedded into the ChromaDB collection.

RAG Architecture

The complete pipeline is:

Policy Documents
      ↓
Ingestion
      ↓
Chunking
      ↓
Embedding
      ↓
ChromaDB Vector Store
      ↓
User Question
      ↓
FastAPI
      ↓
LangGraph
      ↓
classify_intent
      ↓
Conditional Edge
   ↙           ↘
Policy        General
Question      Question
   ↓              ↓
retrieve_and_   direct_answer
answer
   ↓
Top-3 Retrieval
   ↓
Retrieved Context
   ↓
Answer Generation
   ↓
Structured JSON Response
1. Ingestion

ingest.py loads all 8 files from the docs/ directory.

Each document is converted into a chunk suitable for embedding.

2. Embedding

The chunks are embedded using:

all-MiniLM-L6-v2

The resulting vectors are stored in the local ChromaDB collection.

3. Retrieval

retrieve.py embeds the incoming question and performs semantic similarity search against the ChromaDB collection.

The system retrieves the top 3 most similar chunks using vector similarity/cosine similarity.

The retrieved chunks and their source document names are passed to the LangGraph workflow.

4. Generation

The retrieve_and_answer LangGraph node uses the retrieved context to generate the response.

In the required mock mode, the response is deterministic and begins with:

Based on the retrieved context:

The response is based on the most similar retrieved chunk.

For general questions, the direct_answer node returns the fixed mock response without performing retrieval.

LangGraph Workflow

The assistant uses a LangGraph StateGraph with a typed state.

The graph contains three required nodes:

classify_intent
retrieve_and_answer
direct_answer
classify_intent

This node determines whether the question is:

policy_question

or:

general_question

In the default mock mode, classification uses a keyword heuristic.

Policy-related keywords include:

delivery
return
refund
membership
tracking
cancel
gift card
support hours

If a question contains one of these keywords, it is routed to policy_question.

Otherwise, it is routed to general_question.

Conditional Routing

The graph uses a conditional edge after classify_intent.

                 classify_intent
                       |
                 conditional edge
                  /           \
                 /             \
                ↓               ↓
 retrieve_and_answer       direct_answer
retrieve_and_answer

This node:

Embeds the user question.
Retrieves the top 3 relevant chunks from ChromaDB.
Uses the highest-ranked chunk for the deterministic mock response.
Returns the retrieved source document names.
direct_answer

This node handles general questions that do not require policy retrieval.

In mock mode it returns:

I can only answer questions about Zepto policies right now.

No retrieval is performed for this route.

MOCK_LLM Mode

The project uses the MOCK_LLM environment variable.

The default behavior is:

MOCK_LLM unset
       ↓
MOCK_LLM = 1
       ↓
Deterministic mock mode

Mock mode is the required graded baseline.

It does not make an external LLM API call.

The optional real-LLM path is activated only when:

MOCK_LLM=0

In that mode, the optional LLM generation/classification path can be used while retrieval continues to use the local ChromaDB knowledge base.

The default mock mode is sufficient to run and evaluate the complete project without an API key.

Structured Prompt

The optional real-LLM generation path uses a structured prompt following the required:

Role → Context → Task → Format → Length

The prompt also includes:

Role

The assistant is instructed to act as a Zepto policy support assistant.

Context

Only the retrieved Zepto policy context is supplied as grounding information.

Task

The assistant is instructed to answer the user's policy question using the supplied context.

Format

The response is instructed to follow the required answer format.

Length

The response is constrained to a concise answer.

Negative Constraint

The prompt explicitly prevents unsupported information, for example:

Do not answer using information that is not present in the provided context.
Few-shot Example

The prompt also contains an example question and grounded answer demonstrating the expected behavior.

API

The FastAPI application exposes:

POST /ask

Request format:

{
  "question": "What is the return policy?"
}

Response format:

{
  "answer": "...",
  "sources": [
    "doc_02.txt",
    "doc_06.txt",
    "doc_03.txt"
  ],
  "confidence": 1.0
}

The response is validated using a Pydantic schema containing:

answer
sources
confidence
Validation Tests

The API was tested locally with MOCK_LLM left at its default.

Test 1 — Policy Question

Request:

{
  "question": "What is the return policy?"
}

Observed response:

{
  "answer": "Based on the retrieved context: Grocery and perishable items may be reported for a return within 24 hours of delivery if damaged, spoiled, or incorrect; non-perishable packaged items may be returned within seven days of delivery in unop...",
  "sources": [
    "doc_02.txt",
    "doc_06.txt",
    "doc_03.txt"
  ],
  "confidence": 1.0
}

This test demonstrates:

Policy intent classification
Conditional routing
ChromaDB retrieval
Top-3 source retrieval
Grounded mock response
Structured Pydantic response
Test 2 — General Question

Request:

{
  "question": "What is the capital of India?"
}

Observed response:

{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}

This test demonstrates:

General-question classification
Conditional routing to direct_answer
No retrieval for unrelated questions
Fixed mock response
Structured response
Running the Application Locally
1. Activate the virtual environment

From the project root:

.\.venv\Scripts\Activate.ps1
2. Go to the support assistant directory
cd support_assistant
3. Ingest the policy documents
python ingest.py

This loads the 8 policy documents, creates embeddings using all-MiniLM-L6-v2, and stores them in ChromaDB.

4. Start FastAPI
uvicorn main:api --reload --port 8000

The API runs at:

http://127.0.0.1:8000
5. Swagger UI

Open:

http://127.0.0.1:8000/docs

Use the POST /ask endpoint to test questions.

Docker

The module includes a Dockerfile for local containerization.

The Docker container:

Uses Python 3.11
Copies the support assistant application
Installs the required Python packages
Exposes port 7860
Starts FastAPI using the main:api application object
Build the image

Run this command from inside the support_assistant directory:

docker build -t zepto-support-assistant .
Run the container
docker run -p 7860:7860 zepto-support-assistant

The API will then be available at:

http://127.0.0.1:7860

The API endpoint is:

POST /ask

Docker is included as the required local containerization baseline. No cloud deployment is required.

Component Responsibilities
Component	Responsibility
docs/	Stores the 8 Zepto policy documents
ingest.py	Loads documents, chunks text, creates embeddings, and stores vectors
chroma_db/	Local ChromaDB vector database
retrieve.py	Performs semantic similarity retrieval
assistant.py	Implements the LangGraph workflow and intent routing
classify_intent	Classifies policy vs general questions
retrieve_and_answer	Retrieves top-3 chunks and generates the grounded answer
direct_answer	Handles general questions with the fixed mock response
main.py	Provides the FastAPI endpoints
Dockerfile	Defines the local container image
README.md	Documents architecture, execution, validation, and Docker usage
Design Notes

The system uses local/open-source components and does not require paid external services for the required mock-mode implementation.

The policy corpus, embeddings, and ChromaDB vector database are handled locally.

The architecture separates:

Ingestion
    ↓
Embedding
    ↓
Retrieval
    ↓
Generation

This separation makes the knowledge base, retrieval logic, orchestration, API layer, and optional LLM generation easier to understand and maintain.

The required deterministic mock mode ensures that the application can be tested without an external LLM API.

Optional Real-LLM Extension

The project includes an optional real-LLM path controlled by:

MOCK_LLM=0

This extension is not required for the graded baseline.

The default configuration remains deterministic mock mode:

MOCK_LLM unset

or:

MOCK_LLM=1

No API key is required for the default graded implementation.