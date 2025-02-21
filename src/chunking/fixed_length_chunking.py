def fixed_length_chunking(content, chunk_size):
    """
    Splits content into fixed-length chunks of words.

    :param content: The text to be chunked.
    :param chunk_size: Number of words per chunk.
    :return: A list of text chunks.
    """
    words = content.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]
