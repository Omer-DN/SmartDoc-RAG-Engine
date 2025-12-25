from services.rag_service import get_chunks_by_similarity

def test_get_chunks():
    dummy_embedding = [0.1] * 300
    chunks = get_chunks_by_similarity(dummy_embedding, top_k=2)
    assert isinstance(chunks, list)
