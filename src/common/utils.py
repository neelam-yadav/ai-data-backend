from src.crud import get_pipeline_by_id, get_config


def construct_mongo_uri(host, port):
    """
    Constructs the MongoDB URI from the global configuration.

    :param config: Global configuration dictionary
    :return: Formatted MongoDB URI string
    """
    return f"mongodb://{host}:{port}/"


def get_mongodb_config(db, pipeline_id: int):
    """
    Fetches MongoDB configuration from global settings and pipeline ingestion config.
    :param db: Database session
    :param pipeline_id: ID of the pipeline
    :return: MongoDB URI, database name, and collection name
    """
    # Fetch pipeline details
    pipeline = get_pipeline_by_id(db, pipeline_id)
    if not pipeline:
        return {"error": "Pipeline not found"}

    # Fetch global MongoDB settings
    config = get_config(db)
    if not config or not config.mongo_db['host'] or not config.mongo_db['port']:
        return {"error": "Global MongoDB configuration not found"}

    # Construct MongoDB URI
    try:
        mongo_uri = construct_mongo_uri(config.mongo_db['host'], config.mongo_db['port'])
    except ValueError as e:
        return {"error": str(e)}

    mongo_db_name = pipeline.ingestion_config.get("mongodb_database")
    mongo_collection_name = pipeline.ingestion_config.get("mongodb_collection")

    if not mongo_db_name or not mongo_collection_name:
        return {"error": "MongoDB database or collection not set in pipeline"}

    return {"uri": mongo_uri, "db_name": mongo_db_name, "collection_name": mongo_collection_name}


def get_qdrant_config(db, pipeline_id: int):
    """
    Fetches Qdrant configuration from global settings and pipeline processing config.
    :param db: Database session
    :param pipeline_id: ID of the pipeline
    :return: Qdrant configuration dictionary
    """
    # Fetch pipeline details
    pipeline = get_pipeline_by_id(db, pipeline_id)
    if not pipeline:
        return {"error": "Pipeline not found"}

    # Fetch global Qdrant settings
    config = get_config(db)
    if not config or not config.qdrant_db['url']:
        return {"error": "Global Qdrant configuration not found"}

    qdrant_collection = pipeline.processing_config.get("qdrant_db_collection")

    if not qdrant_collection:
        return {"error": "Qdrant collection not set in pipeline"}

    return {"url": config.qdrant_db["url"], "collection": qdrant_collection}


def get_processing_config(db, pipeline_id: int):
    # Fetch pipeline details
    pipeline = get_pipeline_by_id(db, pipeline_id)
    if not pipeline:
        return {"error": "Pipeline not found"}
    return pipeline.processing_config
