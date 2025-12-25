from services.pdf_loader import extract_text_from_pdf
from services.chunk_text import chunk_text

def ingest_pdf(
    pdf_path: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    """
    Pipeline בסיסי:
    PDF → text → chunks
    """
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    return chunks
