# db/models.py
import uuid
from sqlalchemy import Column, String, Text, TIMESTAMP, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from db.session import Base, engine  # Base ו-engine מ־db/session.py

# ---------------------------
# טבלת documents
# ---------------------------
class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # קשר ל־chunks
    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )

# ---------------------------
# טבלת document_chunks
# ---------------------------
class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(300))  # עמודת VECTOR בגודל 300
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # קשר חזרה ל־Document
    document = relationship("Document", back_populates="chunks")

# ---------------------------
# פונקציה ליצירת טבלאות
# ---------------------------
def create_tables():
    # יצירת extension vector אם הוא לא קיים
    with engine.connect() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()

    # יצירת כל הטבלאות
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

# ---------------------------
# הרצה ישירה של הקובץ
# ---------------------------
if __name__ == "__main__":
    create_tables()
