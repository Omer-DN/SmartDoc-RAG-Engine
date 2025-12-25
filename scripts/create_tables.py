# scripts/create_tables.py
from sqlalchemy import create_engine, Column, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
import os
from dotenv import load_dotenv

# טען משתני סביבה
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")

# כתובת חיבור
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# יצירת engine
engine = create_engine(DATABASE_URL, echo=True)

# בדיקה פשוטה שהחיבור תקין
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database();"))
    print("Connected to database:", result.fetchone()[0])

    # ודא שהסכמה public
    conn.execute(text("SET search_path TO public;"))

    # ודא שה־extension vector מותקן
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

# Base class
Base = declarative_base()

# דוגמת טבלה עם VECTOR
class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(UUID(as_uuid=True), primary_key=True)
    document_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(300))  # עכשיו זה Vector בגודל 300
    created_at = Column(TIMESTAMP(timezone=True), server_default="now()")

# יצירת SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# פונקציה ליצירת הטבלאות
def create_tables():
    Base.metadata.drop_all(bind=engine)  # אם רוצים מחיקה והתחלה מחדש
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
