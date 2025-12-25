# tests/test_rag_service.py
import uuid
import pytest
from services.rag_service import add_chunk, get_chunks_by_similarity
from db.models import DocumentChunk

def test_add_and_get_chunks():
    # יצירת ID מזויף למסמך
    dummy_document_id = uuid.uuid4()

    # יצירת chunk עם embedding דמי
    embedding1 = [0.1] * 300
    embedding2 = [0.2] * 300

    chunk1 = add_chunk(dummy_document_id, "Content 1", embedding1)
    chunk2 = add_chunk(dummy_document_id, "Content 2", embedding2)

    # בדיקה שה-chunks נשמרו
    assert chunk1.id is not None
    assert chunk2.id is not None

    # בדיקה שהפונקציה get_chunks_by_similarity מחזירה את ה-top_k הנכון
    results = get_chunks_by_similarity([0.1]*300, top_k=2)
    assert isinstance(results, list)
    assert len(results) <= 2
    # ודא שה-chunk הקרוב ביותר הוא chunk1
    assert results[0].id == chunk1.id
