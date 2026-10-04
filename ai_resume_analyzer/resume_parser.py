"""Read text from PDF and DOCX resume files without saving them permanently."""

from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_text(file_bytes: bytes, file_name: str) -> str:
    """Extract text from an uploaded PDF or DOCX file's in-memory bytes."""
    name = file_name.lower()
    if name.endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".docx"):
        document = Document(BytesIO(file_bytes))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    raise ValueError("Please upload a PDF or DOCX file.")
