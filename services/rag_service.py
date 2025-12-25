# services/rag_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models import DocumentChunk
from db.session import SessionLocal
from typing import List

def get_chunks_by_similarity(embedding: List[float], top_k: int = 5) -> List[DocumentChunk]:
    """
    מחזיר את ה-top_k chunks הקרובים ביותר ל-embedding שניתן
    """
    with SessionLocal() as session:
        # שימוש ב-vector extension של PostgreSQL דרך pgvector
        stmt = (
            select(DocumentChunk)
            .order_by(DocumentChunk.embedding.l2_distance(embedding))  # L2 distance
            .limit(top_k)
        )
        results = session.execute(stmt).scalars().all()
        return results

def add_chunk(document_id, content, embedding):
    """
    מוסיף chunk חדש למסד הנתונים
    """
    with SessionLocal() as session:
        chunk = DocumentChunk(
            document_id=document_id,
            content=content,
            embedding=embedding
        )
        session.add(chunk)
        session.commit()
        session.refresh(chunk)
        return chunk
