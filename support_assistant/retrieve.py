from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "zepto_policy_docs"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


def retrieve_documents(query, top_k=3):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    retrieved_documents = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        similarity = 1 - distance

        retrieved_documents.append(
            {
                "document": document,
                "source": metadata["source"],
                "similarity": similarity,
            }
        )

    return retrieved_documents


if __name__ == "__main__":
    question = "How long do I have to report a damaged or missing item?"

    results = retrieve_documents(question)

    print("\nQuery:")
    print(question)

    print("\nRetrieved documents:")

    for result in results:
        print("-" * 60)
        print(f"Source: {result['source']}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Content: {result['document']}")