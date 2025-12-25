# tests/test_crud.py
import pytest
import uuid
from db.session import SessionLocal, engine, Base
from db import crud, models

# יצירת טבלאות לבדיקה
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    yield session
    session.close()

def test_create_and_get_document(db):
    doc = crud.create_document(db, title="Test Document")
    assert doc.id is not None
    fetched = crud.get_document(db, doc.id)
    assert fetched.title == "Test Document"

def test_create_and_get_chunk(db):
    doc = crud.create_document(db, title="Chunk Doc")
    chunk = crud.create_chunk(db, document_id=doc.id, content="Hello world", embedding="[0.1,0.2,0.3]")
    assert chunk.id is not None
    chunks = crud.get_chunks(db, document_id=doc.id)
    assert len(chunks) == 1
    assert chunks[0].content == "Hello world"

def test_delete_document(db):
    doc = crud.create_document(db, title="Delete Me")
    deleted = crud.delete_document(db, doc.id)
    assert deleted
    assert crud.get_document(db, doc.id) is None
