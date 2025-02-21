from pymongo import MongoClient
from pymongo.errors import PyMongoError

class MongoDBStorage:
    def __init__(self, uri, db_name, collection_name):
        """
        Initialize the MongoDB connection and select the collection.
        :param uri: MongoDB connection URI.
        :param db_name: Name of the MongoDB database.
        :param collection_name: Name of the collection.
        """
        try:
            self.client = MongoClient(uri)
            self.db_name = db_name
            self.collection_name = collection_name
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            self._ensure_database_exists()
            print(f"Connected to MongoDB: {db_name}.{collection_name}")
        except PyMongoError as e:
            raise Exception(f"Failed to connect to MongoDB: {e}")

    def _ensure_database_exists(self):
        """Ensures the database exists by inserting a dummy document and removing it."""
        print(f"Checking if db name: {self.db_name} exists in mongodb")
        if self.db_name not in self.client.list_database_names():
            print(f"db name: {self.db_name} not exists in mongodb. Creating it")
            self.db.create_collection(self.collection_name)
            print(f"Collection: {self.collection_name} created")
            self.collection.insert_one({"temp": "delete_me"})
            self.collection.delete_many({"temp": "delete_me"})  # Clean up

    def store_data(self, data):
        """
        Inserts a single document into the collection.
        :param data: A dictionary representing the document.
        """
        try:
            self.collection.insert_one(data)
            print("Data stored successfully!")
        except PyMongoError as e:
            raise Exception(f"Failed to store data: {e}")

    def bulk_store_data(self, data, batch_size=200):
        """
        Inserts multiple documents into the collection in batches.
        :param data: A list of dictionaries representing documents.
        :param batch_size: Number of documents to insert in each batch.
        """
        try:
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                self.collection.insert_many(batch)
                print(f"Inserted batch {i // batch_size + 1} with {len(batch)} documents.")
        except PyMongoError as e:
            raise Exception(f"Failed to perform bulk insert: {e}")

    def find_data(self, query=None):
        """
        Retrieves documents from the collection based on a query.
        :param query: A dictionary representing the MongoDB query.
        :return: A list of documents matching the query.
        """
        try:
            query = query or {}
            return list(self.collection.find(query))
        except PyMongoError as e:
            raise Exception(f"Failed to retrieve data: {e}")

    def fetch_data_in_batches(self, batch_size=200):
        """
        Fetches data from MongoDB in batches using skip and limit.
        Stops when no more data is available.

        :param batch_size: Number of documents to fetch in each batch.
        :return: A generator yielding batches of documents.
        """
        try:
            total_docs = self.collection.count_documents({})
            for i in range(0, total_docs, batch_size):
                batch = list(self.collection.find({}).skip(i).limit(batch_size))
                if not batch:
                    break  # Stop if no more data is available
                yield batch
        except Exception as e:
            raise Exception(f"Failed to fetch data in batches: {e}")

    def delete_data(self, query):
        """
        Deletes documents from the collection based on a query.
        :param query: A dictionary representing the MongoDB query.
        """
        try:
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} documents.")
        except PyMongoError as e:
            raise Exception(f"Failed to delete data: {e}")

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        try:
            self.client.close()
            print("MongoDB connection closed.")
        except PyMongoError as e:
            raise Exception(f"Failed to close MongoDB connection: {e}")

    def is_file_processed(self, filepath):
        """
        Check if a file has already been processed.

        :param filepath: Filepath to check.
        :return: True if the file is processed, False otherwise.
        """
        result = self.collection.find_one({"metadata.filepath": filepath})
        return result is not None

    def mark_as_processed(self, filepath):
        """
        Mark a file as processed in MongoDB.

        :param filepath: Filepath of the file to update.
        """
        self.collection.update_one(
            {"metadata.filepath": filepath},
            {"$set": {"metadata.processed": True}}
        )

    def fetch_unprocessed_data(self, batch_size=200):
        """
        Fetches unprocessed data from MongoDB in batches.

        :param batch_size: Number of documents to fetch in each batch.
        :return: A generator yielding batches of unprocessed documents.
        """
        try:
            total_docs = self.collection.count_documents({"metadata.processed": False})
            for i in range(0, total_docs, batch_size):
                # Use `skip` and `limit` to create a new cursor for each batch
                batch = list(
                    self.collection.find({"metadata.processed": False})
                    .skip(i)
                    .limit(batch_size)
                )
                if not batch:
                    break
                yield batch
        except Exception as e:
            raise Exception(f"Failed to fetch data in batches: {e}")