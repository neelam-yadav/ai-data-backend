from src.storage import MongoDBStorage, QdrantStorage
from src.processing import clean_batch, generate_embeddings
import copy
from sqlalchemy.orm import Session
from src.common import get_processing_config, get_mongodb_config, get_qdrant_config


def data_processing_pipeline(db: Session, pipeline_id: int):
    """
    Pipeline to fetch data from MongoDB, clean it, chunk it, generate embeddings,
    and load the embeddings into Qdrant vector database.

    :param config: Configuration dictionary with MongoDB and Qdrant details.
    """
    # MongoDB Configuration
    print(f"Starting data processing for pipeline: {pipeline_id}")
    # Fetch MongoDB Configuration
    mongo_config = get_mongodb_config(db, pipeline_id)
    if "error" in mongo_config:
        return {"error": mongo_config["error"]}

    # Fetch Qdrant Configuration
    qdrant_config = get_qdrant_config(db, pipeline_id)
    if "error" in qdrant_config:
        return {"error": qdrant_config["error"]}

    processing_config = get_processing_config(db, pipeline_id)

    # Initialize MongoDB Storage
    mongo_storage = MongoDBStorage(
        uri=mongo_config["uri"],
        db_name=mongo_config["db_name"],
        collection_name=mongo_config["collection_name"]
    )
    qdrant_storage = QdrantStorage(qdrant_config)

    batch_size = 200
    try:
        for batch in mongo_storage.fetch_unprocessed_data(batch_size):
            if not isinstance(batch, list):
                raise ValueError("Expected batch to be a list of documents.")
            if not batch:  # Stop if the batch is empty
                print("No more data to process. Stopping the pipeline.")
                break

            print(f"Fetched batch of size {len(batch)} from MongoDB.")

            # Step 1: Clean the batch
            cleaned_batch = clean_batch(batch)
            print(f"Cleaned batch of size {len(cleaned_batch)}.")

            # Step 2: Generate embeddings
            embeddings = generate_embeddings(cleaned_batch, processing_config)
            # Validate the embeddings
            if not embeddings or not isinstance(embeddings, list):
                print("Error: generate_embeddings returned None or invalid data")
                return {"error": "Embedding generation failed. Ensure input data is correct."}

            # Check for invalid vectors (None, empty, or incorrect format)
            valid_embeddings = []
            for emb in embeddings:
                if emb.get("embedding") and isinstance(emb["embedding"], list) and len(emb["embedding"]) > 0:
                    valid_embeddings.append(emb)

            if not valid_embeddings:
                print("Error: All generated embeddings are empty or invalid.")
                return {"error": "Generated embeddings are empty or invalid. Check embedding model."}

            print(f"Generated {len(valid_embeddings)} valid embeddings.")

            qdrant_storage.upsert_documents(valid_embeddings)
            print(f"Loaded {len(valid_embeddings)} embeddings into Qdrant.")

            # Step 4: Mark documents as processed
            # for doc in batch:
            #     mongo_storage.mark_as_processed(doc["metadata"]["filepath"])
        return {"status": "success", "message": "Data processing completed successfully"}

    except Exception as e:
        print(f"Error in data processing pipeline: {e}")
        return {"error": f"Failed to process data: {str(e)}"}
    finally:
        mongo_storage.close_connection()
        print("MongoDB connection closed.")
