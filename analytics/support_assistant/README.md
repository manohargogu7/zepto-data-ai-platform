Zepto Support Assistant
Overview

This module implements a Retrieval-Augmented Generation (RAG) based support assistant for Zepto policy questions.

The system retrieves relevant policy documents from a local ChromaDB vector database and uses the retrieved context to generate a grounded response.

Architecture

User Question
→ FastAPI
→ LangGraph Assistant
→ Policy Retrieval
→ ChromaDB
→ Retrieved Context
→ Response

Components
docs/ — Zepto policy documents used as the knowledge base
ingest.py — Loads documents, creates embeddings, and indexes them in ChromaDB
retrieve.py — Performs semantic similarity search
assistant.py — LangGraph-based assistant workflow
main.py — FastAPI API
chroma_db/ — Local vector database
Knowledge Base

The assistant uses 8 policy documents covering topics including:

Delivery and serviceable locations
Returns and refunds
Order cancellation
Damaged or missing items
Payments and wallet-related policies
Customer support
Other Zepto support policies
Retrieval

The documents are embedded using a Sentence Transformers model and stored in ChromaDB.

The retriever returns the most relevant documents for each user question and provides source document names with the response.

API

The FastAPI application exposes:

POST /ask

Example request:

{
  "question": "Can I cancel my order after it is out for delivery?"
}

Example response:

{
  "answer": "Based on the retrieved context: Orders can be cancelled from the 'My Orders' section of the Zepto app up to the point when the order status changes to 'Out for Delivery'. Once the order is out for delivery, cancellation is no longer possible.",
  "sources": [
    "doc_03.txt"
  ],
  "confidence": 1.0
}
GET /

Health-check endpoint confirming that the API is running.

Validation Tests

The API was tested with:

Damaged or missing item policy question
Order cancellation policy question
Unrelated/general question

The policy questions successfully returned retrieved source documents and grounded answers.

For unrelated questions, the assistant returned:

I can only answer questions about Zepto policies right now.

with an empty source list.

Running the Application

From the project root:

python analytics\support_assistant\ingest.py

Then start the API:

uvicorn analytics.support_assistant.main:api --reload

Open the Swagger interface:

http://127.0.0.1:8000/docs

Use the POST /ask endpoint to test the assistant.

Design Notes

The system uses local/open-source components and does not require paid external services.

The vector database and policy documents are stored locally within the project.