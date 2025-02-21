import logging
import os
from pymongo.errors import DuplicateKeyError
from PyPDF2 import PdfReader
from docx import Document


def ingest_files(folder_path, mongo_storage):
    data = []
    print(f"Processing dir: {folder_path}")
    for root, _, files in os.walk(folder_path):
        for file in files:
            print(f"Processign file: {file}")
            file_path = os.path.join(root, file)
            # Check if the file is already processed
            if mongo_storage.is_file_processed(file_path):
                print(f"File:{file_path} is already ingested")
                continue

            print(f"Ingesting file:{file_path}")
            ext = os.path.splitext(file_path)[1].lower()
            if ext == ".pdf":
                content = ingest_pdf(file_path)
            elif ext == ".txt":
                content = ingest_text(file_path)
            else:
                print(f"Unsupported file type: {file_path}")
                continue

            # Add metadata and mark as unprocessed
            data.append({
                "content": content,
                "metadata": {
                    "filepath": file_path,
                    "filename": file,
                    "processed": False  # Mark as unprocessed
                }
            })
    return data


def ingest_docx(file_path):
    doc = Document(file_path)
    content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return content


def ingest_pdf(file_path):
    """
    Extracts text from a PDF file.
    :param file_path: Path to the PDF file.
    :return: Dictionary containing file metadata and content.
    """
    try:
        reader = PdfReader(file_path)
        content = ''
        for page in reader.pages:
            content += page.extract_text()
        print(f"Processed PDF file:{file_path}")
        logging.info(f"Processed PDF file:{file_path}")
        return content
    except Exception as e:
        raise Exception(f"Failed to ingest PDF: {e}")


def ingest_text(file_path):
    """
    Reads content from a plain text file.
    :param file_path: Path to the text file.
    :return: Dictionary containing file metadata and content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        logging.info(f"Processed text file:{file_path}")
        print(f"Processed text file:{file_path}")
        return content
    except Exception as e:
        raise Exception(f"Failed to ingest text file: {e}")