from src.ingestion import ingest_files, ingest_confluence, ingest_database, ingest_logs, ingest_datalake#, ingest_stream
from src.processing import enrich_metadata, standardize_data
from src.storage import MongoDBStorage
from src.common import logger, construct_mongo_uri, get_mongodb_config
from src.crud import get_pipeline_by_id, get_config, get_pipeline_data_sources
from sqlalchemy.orm import Session


def run_data_ingestion(db: Session, pipeline_id: int):
    try:
        # Fetch pipeline ingestion config
        print(f"Fetching pipeline: {pipeline_id}")
        mongo_config = get_mongodb_config(db, pipeline_id)

        if "error" in mongo_config:
            return {"error": mongo_config["error"]}

        # Initialize MongoDB storage
        mongo_storage = MongoDBStorage(
            uri=mongo_config["uri"],
            db_name=mongo_config["db_name"],
            collection_name=mongo_config["collection_name"]
        )

        all_data = []
        data_sources = get_pipeline_data_sources(db, pipeline_id)
        if "error" in data_sources:
            return {"error": data_sources["error"]}

        print("Start ingesting")
        for source in data_sources:
            print(f"ingesting source: {source}")
            try:
                if source["type"] == "file":
                    data = ingest_files(source["config"]["folder_path"], mongo_storage)
                elif source["type"] == "confluence":
                    data = ingest_confluence(source["api_url"], source["auth"])
                elif source["type"] == "database":
                    data = ingest_database(source["connection"], source["query"])
                elif source["type"] == "log":
                    data = ingest_logs(source["file_path"])
                elif source["type"] == "datalake":
                    data = ingest_datalake(source["bucket_name"], source["prefix"])
                # elif source["type"] == "stream":
                #     data = ingest_stream(source["bootstrap_servers"], source["topic"], source["group_id"])
                else:
                    logger.warning(f"Unsupported source type: {source['type']}")
                    continue

                # Step 2: Enrich metadata
                print("Enriching Metadata")
                enriched_data = enrich_metadata(data, source)
                # Step 3: Standardize data
                print("Standardizing data structure")
                standardized_data = [standardize_data(item) for item in enriched_data]
                # Step 4: Add to all_data for bulk storage
                print("Add to list for insertion")
                all_data.extend(standardized_data)

            except Exception as e:
                logger.error(f"Error processing {source['name']}: {e}")

        # Perform bulk insert in batches
        print("Bulk insert")
        mongo_storage.bulk_store_data(all_data, batch_size=200)

        # Close the connection after the pipeline is complete
        mongo_storage.close_connection()
        return {"status": "success", "message": "Data ingestion completed successfully"}

    except Exception as e:
        logger.error(f"Data ingestion failed: {str(e)}")
        return {"error": f"Data ingestion failed: {str(e)}"}
