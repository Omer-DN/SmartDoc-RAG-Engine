from services.chunk_text import chunk_text

def test_chunk_text_basic():
    text = "A" * 1200
    chunks = chunk_text(text, chunk_size=500, overlap=50)

    assert len(chunks) == 3
    assert all(len(c) <= 500 for c in chunks)

def test_chunk_overlap():
    text = "ABCDEFG" * 100
    chunks = chunk_text(text, chunk_size=100, overlap=10)

    assert chunks[0][-10:] == chunks[1][:10]
