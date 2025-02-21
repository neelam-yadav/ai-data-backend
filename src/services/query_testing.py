# File: src/query_testing.py
from src.common import get_qdrant_config, get_processing_config
from src.storage.qdrant_storage import QdrantStorage
from sentence_transformers import SentenceTransformer
import numpy as np


def test_retrieval(db, pipeline_id, query):
    """
    Fetch relevant embeddings from Qdrant and evaluate AI readiness.

    :param db: Database session
    :param pipeline_id: Pipeline ID
    :param query: Search query
    :return: Retrieval results with AI readiness evaluation
    """
    print(f"🔍 Querying for: {query}")

    # Fetch Qdrant Configuration
    qdrant_config = get_qdrant_config(db, pipeline_id)
    if "error" in qdrant_config:
        return {"error": qdrant_config["error"]}

    # Initialize Qdrant storage
    qdrant = QdrantStorage(qdrant_config)

    processing_config = get_processing_config(db, pipeline_id)

    # Load embedding model
    model_name = processing_config.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
    embedding_model = SentenceTransformer(model_name)

    # Generate embedding for the query
    query_embedding = embedding_model.encode(query).tolist()  # Convert to list

    # Perform vector search using `query_points`
    retrieved = qdrant.client.search(
        collection_name=qdrant.collection_name,
        query_vector=query_embedding,
        limit=10,  # Fetch top 10 results
        with_vectors=False,  # We only need payloads
        score_threshold=0.5  # Optional: Adjust similarity threshold
    )

    if not retrieved:
        return {"error": "No results found"}

    # **Filter results above similarity threshold (e.g., 0.7)**
    high_quality_results = [doc for doc in retrieved if doc.score >= 0.7]

    # **Compute AI Readiness Metrics**
    retrieved_docs = len(retrieved)
    retrieved_above_threshold = len(high_quality_results)

    # **Compute Top-K Accuracy**
    accuracy = sum(1 for doc in retrieved[:10] if query.lower() in doc.payload.get("filename", "").lower()) / len(
        retrieved[:10])

    # **Compute Semantic Similarity Score**
    retrieved_embeddings = np.array([doc.vector for doc in retrieved if doc.vector is not None])
    similarity_scores = np.dot(retrieved_embeddings, query_embedding) / (
            np.linalg.norm(retrieved_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    avg_similarity = np.mean(similarity_scores)

    # Extract the first retrieved document text (if available)
    first_result = retrieved[0].payload.get("text", "N/A") if retrieved else "N/A"

    # **Print Debugging Information**
    print(f"📌 Retrieved Documents (Top {retrieved_docs}) with Similarity Scores:")
    for idx, doc in enumerate(retrieved[:10]):  # Show only top 10
        filename = doc.payload.get("filename", "Unknown")
        score = doc.score
        print(f"Rank {idx + 1} | Score: {score:.4f} | Filename: {filename}")

    return {
        "retrieved_docs": retrieved_docs,
        "retrieved_above_threshold": retrieved_above_threshold,
        "top_10_accuracy": accuracy,
        "avg_similarity_score": avg_similarity,  # AI readiness metric
        "first_result": first_result
    }
