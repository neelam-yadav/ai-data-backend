from src.chunking import (fixed_length_chunking, sliding_window_chunking, sentence_based_chunking,
                          punctuation_based_chunking, semantic_chunking)


def get_chunks(content, method, chunk_size=100, overlap=0, num_topics=5):
    """
    Dispatches the appropriate chunking method.

    :param content: The text to be chunked.
    :param method: The chunking method (e.g., 'fixed_length', 'sliding_window').
    :param chunk_size: Size of each chunk.
    :param overlap: Overlap size for sliding window chunking.
    :param num_topics: Number of topics for semantic chunking.
    :return: A list of text chunks.
    """
    if method == "fixed_length":
        return fixed_length_chunking(content, chunk_size)
    elif method == "sliding_window":
        return sliding_window_chunking(content, chunk_size, overlap)
    elif method == "sentence_based":
        return sentence_based_chunking(content)
    elif method == "punctuation_based":
        return punctuation_based_chunking(content)
    elif method == "semantic":
        return semantic_chunking(content, num_topics, chunk_size)
    else:
        raise ValueError(f"Invalid chunking method: {method}")
