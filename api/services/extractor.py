import os, requests, tempfile
from azure.storage.blob import BlobServiceClient
from PyPDF2 import PdfReader
from docx import Document
from config import BLOB_CONN_STR

def upload_to_blob(file, conn_str: str) -> str:
    blob_service = BlobServiceClient.from_connection_string(conn_str)
    container = blob_service.get_container_client("uploads")
    container.create_container(exist_ok=True)
    blob = container.get_blob_client(file.filename)
    blob.upload_blob(file.stream, overwrite=True)
    return blob.url

def extract_text_from_blob(blob_url: str) -> str:
    """
    Tải file từ blob_url rồi extract text:
      - PDF: PyPDF2
      - DOCX: python-docx
      - TXT: decode utf-8
    """
    resp = requests.get(blob_url)
    ext = os.path.splitext(blob_url)[1].lower()
    data = resp.content

    if ext == '.pdf':
        reader = PdfReader(data)
        return "\n".join([page.extract_text() or "" for page in reader.pages])

    elif ext in ('.docx',):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        tmp.write(data); tmp.close()
        doc = Document(tmp.name)
        os.unlink(tmp.name)
        return "\n".join([p.text for p in doc.paragraphs])

    else:  # .txt hoặc khác
        return data.decode('utf-8', errors='ignore')
