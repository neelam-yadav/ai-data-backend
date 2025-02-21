def ingest_logs(file_path):
    with open(file_path, "r") as file:
        logs = file.readlines()
    return {"content": "".join(logs), "source": file_path}
