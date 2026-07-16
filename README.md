# Enterprise Banking AI Assistant

Enterprise Banking AI Assistant is an AI-powered banking application built using Python, Streamlit, FastAPI, Retrieval-Augmented Generation (RAG), ChromaDB, Sentence Transformers, and Ollama (Llama 3.1).

The project demonstrates how enterprise applications can combine REST APIs, document retrieval, and Large Language Models to provide intelligent, context-aware banking assistance.

---

# Features

- AI-powered Banking Chat Assistant
- Streamlit Web Interface
- FastAPI REST APIs
- Retrieval-Augmented Generation (RAG)
- PDF Knowledge Base
- ChromaDB Vector Database
- Sentence Transformer Embeddings
- Ollama (Llama 3.1)
- Enterprise Architecture

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Programming Language | Python 3.11+ |
| User Interface | Streamlit |
| Backend | FastAPI |
| Large Language Model | Ollama (Llama 3.1) |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Embedding Model | Sentence Transformers (all-MiniLM-L6-v2) |
| PDF Loader | PyPDF |
| Application Server | Uvicorn |

---

# Project Structure

```text
AI Python/
│
├── app.py
├── api.py
├── requirements.txt
│
├── data/
│   ├── HomeLoan.pdf
│   ├── CreditCard.pdf
│   ├── KYC.pdf
│   ├── SavingsAccount.pdf
│   └── FAQ.pdf
│
├── rag/
│   ├── ingest.py
│   └── retriever.py
│
├── chromadb/
│
└── venv/
```

---

# Architecture

```text
                   User

                     │

                     ▼

             Streamlit UI

                     │

            Intent Detection

      ┌──────────┬───────────┬───────────┐

      ▼          ▼           ▼

   FastAPI      RAG        Ollama

      │          │           │

      ▼          ▼           ▼

 Banking API  ChromaDB    Llama 3.1

                  │

                  ▼

          PDF Documents
```

---

# RAG Workflow

```text
PDF Documents
      │
      ▼
Load Documents
      │
      ▼
Chunking
      │
      ▼
Embeddings
      │
      ▼
ChromaDB
      │
      ▼
Retriever
      │
      ▼
Llama 3.1
      │
      ▼
Generated Response
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd AI-Python
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Install Ollama

Download Ollama from:

https://ollama.com/download

Pull the Llama 3.1 model:

```bash
ollama pull llama3.1
```

---

# Build the Vector Database

```bash
python rag/ingest.py
```

Expected output:

```text
Loaded 5 PDF pages

Created 5 chunks

Vector Database Created Successfully
```

---

# Run FastAPI

```bash
uvicorn api:app --reload
```

Open the Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Run Streamlit

```bash
streamlit run app.py
```

Open the application:

```text
http://localhost:8501
```

---

# Demo Questions

## FastAPI

```text
What is my account balance?

Show IFSC code.

Show branch details.

Show loan information.
```

---

## RAG

```text
What documents are required for Home Loan?

Explain KYC.

What is the Home Loan interest rate?

What is the minimum balance for a Savings Account?
```

---

## LLM

```text
Explain Artificial Intelligence.

Write an email requesting a Home Loan.

Summarize Generative AI.
```

---

# REST API Endpoints

| Endpoint | Description |
|----------|-------------|
| GET /balance | Customer Balance |
| GET /loan | Loan Details |
| GET /ifsc | IFSC Information |
| GET /branch | Branch Details |

---

# Application Components

## Streamlit

Provides the interactive chat interface.

## FastAPI

Provides enterprise REST APIs.

## RAG

Retrieves relevant banking documents.

## ChromaDB

Stores vector embeddings for semantic search.

## Ollama

Runs the Llama 3.1 model locally.

## Sentence Transformers

Generates embeddings for document retrieval.

---

# Benefits

- Enterprise-ready architecture
- REST API integration
- Document-based knowledge retrieval
- AI-powered conversational interface
- Local LLM deployment
- Reduced hallucinations using RAG
- Modular and extensible design

---

# Future Enhancements

- IBM Granite models using watsonx.ai
- LangGraph-based agent orchestration
- Model Context Protocol (MCP) integration
- Multi-agent architecture
- Authentication and authorization
- Role-based access control
- Docker and Kubernetes deployment
- PostgreSQL integration
- Real banking system APIs

---

# Architecture Summary

```text
User
   │
   ▼
Streamlit UI
   │
   ▼
Intent Detection
   │
   ▼
FastAPI / RAG / LLM
   │
   ▼
Enterprise Response
```

---

# Author

Kalyan Samanta

Enterprise AI Developer

Python | FastAPI | Streamlit | LangChain | RAG | ChromaDB | Ollama | Generative AI

---

# License

MIT License

---

# Acknowledgements

- IBM Skills Network
- Ollama
- LangChain
- ChromaDB
- Streamlit
- FastAPI
- Sentence Transformers