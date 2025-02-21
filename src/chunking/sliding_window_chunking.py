def sliding_window_chunking(content, chunk_size, overlap):
    """
    Splits content into overlapping chunks using a sliding window.

    :param content: The text to be chunked.
    :param chunk_size: Number of words per chunk.
    :param overlap: Number of overlapping words between chunks.
    :return: A list of overlapping text chunks.
    """
    words = content.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size - overlap)
    ]
