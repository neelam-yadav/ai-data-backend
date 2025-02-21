from nltk.tokenize import sent_tokenize

def sentence_based_chunking(content):
    """
    Splits content into chunks based on sentences.

    :param content: The text to be chunked.
    :return: A list of sentence-based chunks.
    """
    return sent_tokenize(content)
