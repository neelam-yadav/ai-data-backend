# File: src/common/embedding_model.py
from sentence_transformers import SentenceTransformer

# Load model once globally
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # Small & fast


def generate_embedding(text):
    """
    Generates an embedding for a given text using SentenceTransformers.

    Args:
        text (str): Input text.

    Returns:
        list: Embedding vector.
    """
    return model.encode(text).tolist()  # Convert to list for JSON compatibility
