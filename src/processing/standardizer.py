def standardize_data(data):
    """
    Standardizes the structure of a data item.

    :param data: A dictionary representing enriched data.
    :return: A dictionary with standardized fields.
    """
    standardized_data = {
        "content": data.get("content", "").strip(),  # Ensure content is cleaned
        "metadata": {
            "filepath": data["metadata"].get("filepath", "unknown"),
            "filename": data["metadata"].get("filename", "unknown"),
            "processed": data["metadata"].get("processed", False),  # Preserve processed status
            "datasource": data["metadata"].get("datasource", "unknown"),
            "datasource_type": data["metadata"].get("datasource_type", "unknown"),
            "created_date": data["metadata"].get("created_date", "unknown"),
        }
    }
    return standardized_data

