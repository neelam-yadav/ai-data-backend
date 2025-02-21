import numpy as np
import umap
import matplotlib.pyplot as plt

from src.common import get_qdrant_config
from src.crud import get_pipeline_by_id
from src.storage import QdrantStorage


def cluster_embeddings(db, pipeline_id):
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
    if len(embeddings) == 0:
        return {"error": "No embeddings found"}

    vectors = np.array([e["vector"] for e in embeddings])
    reducer = umap.UMAP(n_neighbors=10, min_dist=0.1, metric="cosine")
    embedding_2d = reducer.fit_transform(vectors)

    plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1], alpha=0.5)
    plt.title("Embedding Clustering")
    plt.savefig("clustering_analysis.png")
    return "Clustering visualization saved as clustering_analysis.png"
