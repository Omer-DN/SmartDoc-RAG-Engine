# RAG Backend Project

פרויקט זה הוא מערכת RAG (Retrieval-Augmented Generation) בסיסית ב‑Python, עם **PostgreSQL + pgvector** לאחסון embeddings, שירותי PDF לטעינת מסמכים, ושירותי עיבוד טקסט ל‑chunks.

---

## 📂 ארכיטקטורת הפרויקט

ragBackend/
├── scripts/
│ └── create_tables.py # יצירת טבלאות PostgreSQL ו־extensions
├── services/
│ ├── pdf_loader.py # פונקציות לטעינת PDF והמרת הטקסט
│ ├── text_chunker.py # חיתוך הטקסט ל־chunks
│ ├── ingest_service.py # pipeline להוספת PDF ל־DB
│ └── rag_service.py # פונקציות לשליפת chunks דומים מה‑DB
├── tests/
│ ├── test_pdf_loader.py
│ ├── test_text_chunker.py
│ ├── test_ingest_service.py
│ └── test_rag_service.py
├── .env # משתני סביבה למסד הנתונים
├── requirements.txt
└── README.md


---

## ⚙️ התקנות

### 1️⃣ יצירת סביבת עבודה

```bash
python -m venv venv
source venv/bin/activate       # לינוקס / macOS
venv\Scripts\activate          # Windows
2️⃣ התקנת ספריות
bash
Copy code
pip install -r requirements.txt
דוגמה ל‑requirements.txt עד כה:

php
Copy code
SQLAlchemy
psycopg2-binary
python-dotenv
PyPDF2
pytest
pgvector
3️⃣ התקנת PostgreSQL עם pgvector
אפשרות לוקאלית:
התקנת PostgreSQL (גרסה 16+)

התחברות ל‑psql והתקנת extension:

sql
Copy code
CREATE EXTENSION IF NOT EXISTS vector;
אפשרות Docker:
bash
Copy code
docker run --name pgvector -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d ankane/pgvector:pg16
📝 יצירת טבלאות
bash
Copy code
python scripts/create_tables.py
קוד מרכזי:

python
Copy code
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Text, TIMESTAMP

Base = declarative_base()

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(UUID(as_uuid=True), primary_key=True)
    document_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column("embedding", Text)  # Text בינתיים עד שה-vector עובד
    created_at = Column(TIMESTAMP(timezone=True), server_default="now()")
📄 טעינת PDF וחיתוך ל‑chunks
pdf_loader.py
python
Copy code
from pathlib import Path
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() for page in reader.pages)
text_chunker.py
python
Copy code
def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks
🗄️ Ingest Service
python
Copy code
from services.pdf_loader import extract_text_from_pdf
from services.text_chunker import chunk_text

def ingest_pdf(pdf_path: str):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    # שמירת chunks ב‑DB (לפי DocumentChunk)
    return chunks
🔍 RAG Service
אחראי על שליפת chunks דומים מה‑DB לפי embedding.

משתמש ב‑pgvector ל‑similarity search.

python
Copy code
def get_chunks_by_similarity(embedding, top_k=5):
    # SELECT * FROM document_chunks ORDER BY embedding <-> :embedding LIMIT :top_k
    ...
✅ בדיקות (pytest)
bash
Copy code
pytest tests/test_pdf_loader.py
pytest tests/test_text_chunker.py
pytest tests/test_ingest_service.py
pytest tests/test_rag_service.py
📌 הערות
נכון לעכשיו, embeddings מאוחסנים כ־Text ב‑DB; בעתיד נשתמש ב־pgvector.

ניתן לשלב LLM דרך LangChain בשלב הבא.

