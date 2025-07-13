# genai-doc-assistant/backend/utils/doc_parser.py
import fitz  # PyMuPDF
import os
from fastapi import UploadFile

async def parse_document(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower()

    if ext == ".pdf":
        return await _parse_pdf(file)
    elif ext == ".txt":
        return (await file.read()).decode("utf-8")
    else:
        raise ValueError("Unsupported file format. Only PDF and TXT allowed.")

def clean_text(text: str) -> str:
    return " ".join(text.strip().split())

async def _parse_pdf(file: UploadFile) -> str:
    content = await file.read()

    with open("temp.pdf", "wb") as f:
        f.write(content)

    doc = fitz.open("temp.pdf")
    text = "\n".join([page.get_text() for page in doc])
    doc.close()
    os.remove("temp.pdf")

    return clean_text(text)