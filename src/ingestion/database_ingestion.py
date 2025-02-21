import psycopg2

def ingest_database(config):
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            database=config["database"],
            user=config["user"],
            password=config["password"]
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM your_table")  # Replace with your query
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        raise RuntimeError(f"Error fetching data from database: {str(e)}")
