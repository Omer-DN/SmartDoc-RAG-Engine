from pathlib import Path
from services.pdf_loader import extract_text_from_pdf

def test_extract_text_from_pdf():
    base_dir = Path(__file__).parent
    pdf_path = base_dir / "sample.pdf"

    text = extract_text_from_pdf(pdf_path)

    assert text is not None
    assert len(text.strip()) > 0
