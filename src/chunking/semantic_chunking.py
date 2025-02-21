from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize
from textwrap import wrap
import numpy as np
import nltk

# Ensure NLTK tokenizer is available
nltk.download('punkt_tab')

def semantic_chunking(content, num_topics=5, chunk_size=100):
    """
    Splits content into semantic chunks using topic modeling and embeddings.

    :param content: The text to be chunked.
    :param num_topics: Number of semantic topics to identify.
    :param chunk_size: Size of each semantic chunk.
    :return: A list of semantic chunks.
    """
    # Tokenize sentences
    sentences = sent_tokenize(content)

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # LDA for topic modeling
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda_topics = lda.fit_transform(tfidf_matrix)

    # Cluster sentences into topics
    topic_clusters = {i: [] for i in range(num_topics)}
    for idx, topic in enumerate(np.argmax(lda_topics, axis=1)):
        topic_clusters[topic].append(sentences[idx])

    # Combine sentences into chunks
    chunks = []
    for cluster in topic_clusters.values():
        chunk = " ".join(cluster)
        if len(chunk.split()) > chunk_size:
            chunks.extend(wrap(chunk, chunk_size))  # Ensures balanced chunking
        else:
            chunks.append(chunk)

    return chunks
