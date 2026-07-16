from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_PATH = Path("chromadb")

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

if not CHROMA_PATH.exists():
    print(
        f"⚠️  Warning: '{CHROMA_PATH}' does not exist yet. "
        "Run ingest.py first to build the vector database."
    )

db = Chroma(
    persist_directory=str(CHROMA_PATH),
    embedding_function=embeddings
)

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 10
    }
)


def search_documents(question):
    """
    Retrieve relevant chunks for a question.

    Returns:
        (context: str, sources: list[dict]) on success
        ("", []) if nothing is found or an error occurs
    """

    try:
        docs = retriever.invoke(question)
    except Exception as e:
        print(f"❌ Retrieval error: {e}")
        return "", []

    if not docs:
        return "", []

    context = ""
    sources = []

    for doc in docs:

        context += doc.page_content + "\n\n"

        raw_source = doc.metadata.get("source")
        file_name = Path(raw_source).name if raw_source else "Unknown"

        raw_page = doc.metadata.get("page")
        page_display = raw_page + 1 if isinstance(raw_page, int) else "N/A"

        sources.append(
            {
                "file": file_name,
                "page": page_display
            }
        )

    return context, sources