from sentence_transformers import SentenceTransformer
from src.chunking import get_chunks
import numpy as np
import copy

def generate_embeddings(data, processing_config=None):
    """
    Generates embeddings for a batch of documents using a SentenceTransformer model.

    :param data: A list of documents with `content` fields.
    :param model_name: The name of the embedding model to use.
    :param chunking_config: Configuration for the chunking method.
    :return: A list of documents with embeddings and metadata.
    """
    model_name = processing_config.get("embedding_model", "all-mpnet-base-v2")
    model = SentenceTransformer(model_name)
    results = []

    for doc in data:
        content = doc.get("content", "")
        # Skip if content is empty
        if not content.strip():
            print(f"Skipping document with empty content: {doc.get('metadata', {}).get('filename', 'Unknown')}")
            continue
        # Chunk the content
        chunks = get_chunks(
            content,
            method=processing_config.get("chunking_method", "fixed_length"),
            chunk_size=processing_config.get("chunk_size", 100),
            overlap=processing_config.get("overlap", 50),
            num_topics=processing_config.get("num_topics", 5)
        )

        if not chunks:
            print(
                f"Skipping document '{doc.get('metadata', {}).get('filename', 'Unknown')}' - No valid text chunks found.")
            continue

        # Generate embeddings for each chunk
        try:
            embeddings = model.encode(chunks, show_progress_bar=True)
            if not isinstance(embeddings, np.ndarray) or embeddings.size == 0:
                print(
                    f"Skipping document '{doc.get('metadata', {}).get('filename', 'Unknown')}' - No valid embeddings generated.")
                continue

            print("Preparing embeddings")
            for chunk, embedding in zip(chunks, embeddings):
                if embedding is None or not isinstance(embedding, np.ndarray) or embedding.size == 0:
                    print(f"Skipping invalid embedding for chunk: {chunk[:50]}...")
                    continue  # Skip invalid embeddings

                doc_metadata = copy.deepcopy(doc.get("metadata", {}))
                doc_metadata["text"] = chunk  # ✅ Store chunk text in metadata

                results.append({
                    "content": chunk,
                    "embedding": embedding.tolist(),  # Convert numpy array to list for serialization
                    "metadata": doc_metadata
                })

        except Exception as e:
            print(
                f"Error generating embeddings for document '{doc.get('metadata', {}).get('filename', 'Unknown')}': {str(e)}")

    return results
