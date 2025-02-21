import re

def clean_text(text):
    if not text or not isinstance(text, str):
        return ""

        # Normalize non-ASCII characters
    text = text.encode("ascii", "ignore").decode("utf-8")

    # Remove emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # Flags
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub("", text)

    # Remove extra whitespaces
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    return text


def clean_batch(batch):
    """
    Cleans the contents of a batch of documents.

    :param batch: A list of documents with `content` fields.
    :return: A cleaned batch of documents.
    """
    cleaned_batch = []
    for doc in batch:
        # Ensure the document is a dictionary and has a content field
        if isinstance(doc, dict) and "content" in doc and doc["content"]:
            try:
                doc["content"] = clean_text(doc["content"])
                cleaned_batch.append(doc)
            except Exception as e:
                print(f"Error cleaning document: {e}")
        else:
            print(f"Skipping invalid document: {doc}")
    return cleaned_batch
