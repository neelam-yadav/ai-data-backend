def punctuation_based_chunking(content, delimiter=";"):
    """
    Splits content into chunks based on a punctuation delimiter.

    :param content: The text to be chunked.
    :param delimiter: The punctuation mark to split on.
    :return: A list of punctuation-based chunks.
    """
    return content.split(delimiter)
