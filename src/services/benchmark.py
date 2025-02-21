import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datasets import load_dataset

from src.common import get_qdrant_config, generate_embedding
from src.crud import get_pipeline_by_id
from src.storage import QdrantStorage


def load_benchmark_dataset():
    """
        Loads a benchmark dataset and generates embeddings.

        Returns:
            List of dictionaries with "embedding" and "text".
        """
    # Load a benchmark dataset (MS MARCO / SQuAD / SciDocs)
    dataset = load_dataset("ms_marco", split="train[:1000]")  # Limit for efficiency

    # Convert text into embeddings
    benchmark_data = []
    for sample in dataset:
        embedding = generate_embedding(sample["query"])  # Convert query into vector
        benchmark_data.append({
            "text": sample["query"],
            "embedding": embedding,
            "relevant": True  # Can be adjusted based on dataset labels
        })

    return benchmark_data


def benchmark_embeddings(db, pipeline_id):
    """Compares AI readiness with benchmark datasets"""
    pipeline = get_pipeline_by_id(db, pipeline_id)
    if not pipeline:
        return {"error": "Pipeline not found"}

    # Fetch Qdrant Configuration
    qdrant_config = get_qdrant_config(db, pipeline_id)
    if "error" in qdrant_config:
        return {"error": qdrant_config["error"]}

    # Initialize Qdrant storage
    qdrant = QdrantStorage(qdrant_config)
    # Fetch embeddings
    embeddings = qdrant.fetch_embeddings(qdrant_config["collection"])

    # Load Benchmark Dataset
    dataset = load_benchmark_dataset()
    if len(dataset) == 0:
        return {"error": "Benchmark dataset is empty"}

    # Convert to NumPy array
    vectors = np.array([e["vector"] for e in embeddings])
    dataset_vectors = np.array([sample["embedding"] for sample in dataset])

    # Compute cosine similarity
    similarity_scores = cosine_similarity(vectors, dataset_vectors)

    return {
        "average_similarity": np.mean(similarity_scores),
        "max_similarity": np.max(similarity_scores),
        "min_similarity": np.min(similarity_scores)
    }
