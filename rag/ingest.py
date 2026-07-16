import sys
from pathlib import Path
import shutil

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Configuration #

DATA_PATH = Path("data")
CHROMA_PATH = Path("chromadb")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def main():

    print("=" * 60)
    print("Enterprise Banking RAG")
    print("=" * 60)

    # Validate input folder #
    if not DATA_PATH.exists() or not DATA_PATH.is_dir():
        print(f"Data folder not found: {DATA_PATH.resolve()}")
        print("Create the folder and add PDF files before running this script.")
        sys.exit(1)

    pdf_files = list(DATA_PATH.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in: {DATA_PATH.resolve()}")
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF file(s)")

    try:
        loader = PyPDFDirectoryLoader(str(DATA_PATH))
        documents = loader.load()
    except Exception as e:
        print(f"Failed to load PDFs: {e}")
        sys.exit(1)

    if not documents:
        print("No content could be extracted from the PDFs.")
        sys.exit(1)

    print(f"Loaded {len(documents)} PDF pages")

    # Split into chunks #
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        print("Splitting produced 0 chunks. Aborting.")
        sys.exit(1)

    print(f"Created {len(chunks)} chunks")

    # Build embeddings #
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
    except Exception as e:
        print(f"Failed to load embedding model '{EMBEDDING_MODEL}': {e}")
        sys.exit(1)

    # Rebuild the vector store #
    if CHROMA_PATH.exists():
        shutil.rmtree(CHROMA_PATH)

    try:
        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(CHROMA_PATH)
        )
    except Exception as e:
        print(f"Failed to build vector database: {e}")
        sys.exit(1)

    print("\nVector Database Created Successfully")
    print(f"   Location: {CHROMA_PATH.resolve()}")


if __name__ == "__main__":
    main()