from datetime import datetime

def enrich_metadata(data, source_config):
    """
    Enriches the metadata of ingested data with additional details.

    :param data: A list of dictionaries representing the ingested data.
    :param source_config: Configuration dictionary for the data source.
    :return: A list of dictionaries with enriched metadata.
    """
    enriched_data = []
    for item in data:
        # Ensure metadata fields exist
        metadata = item.get("metadata", {})
        enriched_metadata = {
            "filepath": metadata.get("filepath", "unknown"),
            "filename": metadata.get("filename", "unknown"),
            "processed": metadata.get("processed", False),  # Preserve processed status
            "datasource": source_config.get("name", "unknown"),
            "datasource_type": source_config.get("type", "unknown"),
            "created_date": datetime.now().isoformat(),  # Add timestamp
        }
        enriched_data.append({
            "content": item.get("content", ""),  # Preserve content
            "metadata": enriched_metadata
        })
    return enriched_data
