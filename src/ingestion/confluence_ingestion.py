import requests

def ingest_confluence(api_url, auth):
    """
    Fetches content from Confluence pages.
    :param api_url: Confluence API URL.
    :param auth: Authentication credentials (username and API token).
    :return: List of Confluence page content.
    """
    response = requests.get(api_url, auth=(auth["username"], auth["api_token"]))
    response.raise_for_status()
    pages = response.json()["results"]
    return [{"source": "confluence", "content": page["body"]["storage"]["value"], "metadata": {"id": page["id"], "title": page["title"]}} for page in pages]
