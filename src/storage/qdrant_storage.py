from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct, Filter
import numpy as np


class QdrantStorage:
    """
    A storage manager for handling operations with Qdrant vector database.
    Provides methods for initializing connection, ensuring collections, and inserting embeddings.
    """

    def __init__(self, config):
        """
        Initializes the Qdrant client with the given configuration.

        :param config: Dictionary containing 'url', 'api_key', and 'collection'.
        """
        self.client = QdrantClient(url=config["url"], api_key=config.get("api_key", None))
        self.collection_name = config["collection"]

    def ensure_collection_exists(self, vector_size):
        """
        Ensures the Qdrant collection exists with the correct configuration.

        :param vector_size: The dimensionality of the vectors to be stored.
        """
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance="Cosine"  # Distance metric for similarity search
                )
            )
            print(f"Collection '{self.collection_name}' created.")
        else:
            print(f"Collection '{self.collection_name}' already exists.")

    def upsert_documents(self, data, batch_size=500):
        """
        Inserts documents into Qdrant in batches, ensuring no duplicates.

        :param data: List of documents containing 'embedding' and 'metadata'.
        :param batch_size: Number of points to insert in each batch.
        """
        try:
            # Ensure collection is ready before inserting
            if not data:
                print("No data to insert.")
                return

            self.ensure_collection_exists(vector_size=len(data[0]["embedding"]))

            # Prepare points to insert
            points_to_insert = []
            for index, doc in enumerate(data):
                # Check if the point already exists
                existing_points = self.client.scroll(
                    collection_name=self.collection_name,
                    scroll_filter=Filter(
                        must=[{"key": "filepath", "match": {"value": doc["metadata"]["filepath"]}}]
                    ),
                    limit=1
                )

                if not existing_points[0]:  # If point does not exist, add it
                    points_to_insert.append(
                        PointStruct(
                            id=index,
                            vector=doc["embedding"],
                            payload=doc["metadata"]
                        )
                    )

            # Insert in batches
            for i in range(0, len(points_to_insert), batch_size):
                batch = points_to_insert[i:i + batch_size]
                self.client.upsert(collection_name=self.collection_name, points=batch)
                print(f"Inserted batch {i // batch_size + 1} with {len(batch)} points.")

        except Exception as e:
            raise Exception(f"Failed to load data into Qdrant: {e}")

    def query_points(self, query_embedding, top_k=10):
        """
        Searches for the top-K most relevant documents using `query_points` API.

        :param query_embedding: Vector representation of the query.
        :param top_k: Number of top results to retrieve.
        :return: List of matching documents with metadata and scores.
        """
        try:
            results = self.client.query_points(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )

            return [
                {
                    "vector": np.array(result.vector),
                    "score": result.score,
                    "metadata": result.payload
                }
                for result in results
            ]

        except Exception as e:
            raise Exception(f"Failed to perform query in Qdrant: {e}")

    def fetch_embeddings(self, collection_name):
        """
        Fetch all embeddings from a collection in Qdrant.

        :param collection_name: Name of the collection to fetch embeddings from.
        :return: List of embeddings with metadata.
        """
        try:
            response = self.client.scroll(
                collection_name=collection_name,
                limit=10000,  # Adjust limit based on your needs
                with_payload = True,
                with_vectors = True
            )

            embeddings = [
                {"vector": point.vector, "metadata": point.payload}
                for point in response[0]
            ]

            return embeddings

        except Exception as e:
            print(f"Error fetching embeddings from Qdrant: {e}")
            return []

