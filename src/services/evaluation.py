import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.storage.qdrant_storage import QdrantStorage
from src.common import get_qdrant_config

def evaluate_embeddings(db, pipeline_id):
    """
    Evaluate the embeddings stored in Qdrant to check AI readiness.

    :param db: Database session
    :param pipeline_id: Pipeline ID
    :return: Evaluation metrics for embeddings
    """
    # Fetch Qdrant configuration
    qdrant_config = get_qdrant_config(db, pipeline_id)
    if "error" in qdrant_config:
        return {"error": qdrant_config["error"]}

    # Initialize Qdrant Storage
    qdrant = QdrantStorage(qdrant_config)

    # Fetch embeddings
    embeddings = qdrant.fetch_embeddings(qdrant_config["collection"])
    print(embeddings)

    if not embeddings:
        return {"error": "No embeddings found"}

    # Filter valid numeric embeddings
    valid_vectors = []
    for e in embeddings:
        vector = e.get("vector")
        if vector is not None and isinstance(vector, list) and len(vector) > 0:
            try:
                vec = np.array(vector, dtype=np.float32)
                if np.all(np.isfinite(vec)) and not np.isnan(vec).any():
                    valid_vectors.append(vec)
            except Exception:
                continue

    if not valid_vectors:
        return {"error": "No valid numeric embeddings found. Check data processing pipeline."}

    vectors = np.array(valid_vectors)
    print("Valid Embeddings:", valid_vectors[:5])

    # Ensure embeddings are 2D
    if vectors.ndim == 1 or vectors.shape[0] == 1:
        vectors = vectors.reshape(1, -1)  # Ensure a proper shape

    # Compute cosine similarity
    try:
        similarity_matrix = cosine_similarity(vectors)
    except ValueError as e:
        return {"error": f"Failed to compute similarity: {str(e)}"}

    # Compute AI readiness metrics
    avg_similarity = np.mean(similarity_matrix)
    sparsity_ratio = np.sum(similarity_matrix < 0.5) / similarity_matrix.size

    return {
        "average_similarity": float(avg_similarity),  # Ensure Python native float
        "sparsity_ratio": float(sparsity_ratio),  # Ensure Python native float
        "embedding_count": len(valid_vectors),
    }
