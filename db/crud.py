# db/crud.py
import uuid
from sqlalchemy.orm import Session
from db.models import Document, DocumentChunk

# -------------------
# Document CRUD
# -------------------
def create_document(db: Session, title: str) -> Document:
    doc = Document(title=title)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_document(db: Session, doc_id: uuid.UUID) -> Document | None:
    return db.query(Document).filter(Document.id == doc_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Document).offset(skip).limit(limit).all()

def delete_document(db: Session, doc_id: uuid.UUID) -> bool:
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        return False
    db.delete(doc)
    db.commit()
    return True

# -------------------
# DocumentChunk CRUD
# -------------------
def create_chunk(db: Session, document_id: uuid.UUID, content: str, embedding=None) -> DocumentChunk:
    chunk = DocumentChunk(document_id=document_id, content=content, embedding=embedding)
    db.add(chunk)
    db.commit()
    db.refresh(chunk)
    return chunk

def get_chunks(db: Session, document_id: uuid.UUID):
    return db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).all()
