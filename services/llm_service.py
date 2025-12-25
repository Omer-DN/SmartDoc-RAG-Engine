from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import PGVector
from langchain.prompts import PromptTemplate
from services.rag_service import get_chunks_by_similarity

# הגדרת LLM (נשתמש ב-ChatOpenAI)
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo"
)

def ask_question(question: str, top_k: int = 5) -> str:
    """
    מקבל שאלה, שולף chunks דומים מה-DB ומחזיר תשובה מה-LLM
    """
    # שליפת chunks דומים (אפשר להכניס embeddings אמיתיים כאן)
    chunks = get_chunks_by_similarity([], top_k=top_k)

    # הגדרת PGVector כ-vectorstore
    vectorstore = PGVector(
        table_name="document_chunks",
        embedding_function=lambda x: x,  # כאן אפשר לשלב embedding אמיתי
        connection_string="postgresql://postgres:postgres@localhost:5432/ragdb"
    )

    # בניית chain של RetrievalQA
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": top_k})
    )

    # הרצת השאלה
    return qa.run(question)
