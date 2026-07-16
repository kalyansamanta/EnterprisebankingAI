import streamlit as st
import requests
from datetime import datetime
from pathlib import Path

from ollama import chat
from rag.retriever import search_documents

# Configuration #

MODEL_NAME = "llama3.1"
API_URL = "http://127.0.0.1:8000"
DATA_PATH = Path("data")  # must match ingest.py's DATA_PATH

# Streamlit Configuration

st.set_page_config(
    page_title="Enterprise Banking AI Assistant",
    page_icon="🏦",
    layout="wide"
)

# Sidebar

st.sidebar.title("🏦 Enterprise Banking AI")

st.sidebar.success(f"Model : {MODEL_NAME}")

st.sidebar.markdown("---")

st.sidebar.subheader("Demo Features")

st.sidebar.write("🤖 AI Chat")
st.sidebar.write("🏦 FastAPI Integration")
st.sidebar.write("📄 RAG Knowledge Base")
st.sidebar.write("💰 Account Balance")
st.sidebar.write("🏢 Branch Information")
st.sidebar.write("🏦 IFSC Lookup")
st.sidebar.write("🏠 Loan Information")
st.sidebar.write("📚 PDF Search")

st.sidebar.markdown("---")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Main Page #

st.title("🏦 Enterprise Banking AI Assistant")
st.caption("Powered by Streamlit + Ollama + FastAPI + RAG")
st.markdown("---")

# Initialize Session #

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_source_downloads(sources, key_prefix):
    """Show each retrieved source as a clickable download button for the actual PDF."""

    for i, source in enumerate(sources):

        file_path = DATA_PATH / source["file"]

        if file_path.exists():
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label=f"{source['file']} | Page {source['page']}",
                data=pdf_bytes,
                file_name=source["file"],
                mime="application/pdf",
                key=f"{key_prefix}_src_{i}"
            )
        else:
            st.warning(f"Source file not found on disk: {source['file']}")

# Display Previous Messages

for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources") or []
            if sources:
                st.markdown("### 📚 Retrieved Documents")
                render_source_downloads(sources, key_prefix=f"hist_{idx}")

            st.download_button(
                label="⬇️ Download this answer",
                data=message["content"],
                file_name=f"banking_answer_{message.get('timestamp', idx)}.md",
                mime="text/markdown",
                key=f"download_history_{idx}"
            )

# Chat Input #

prompt = st.chat_input("Ask your banking question...")

# Process Only If User Entered Something #

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert to lowercase for routing
    question = prompt.lower()

    # Default containers so later sections never hit NameError
    sources = []
    is_rag_query = (
        "document" in question
        or "documents" in question
        or "kyc" in question
        or "home loan" in question
        or "credit card" in question
        or "savings account" in question
        or "eligibility" in question
    )
    is_api_query = (
        "balance" in question
        or "branch" in question
        or "ifsc" in question
        or "loan details" in question
        or "interest rate" in question
        or "loan amount" in question
    )

    # FASTAPI - Account Balance #

    if "balance" in question:
        st.info("Calling Banking API...")
        try:
            response = requests.get(f"{API_URL}/balance")
            response.raise_for_status()
            data = response.json()
            answer = f"""
## 💰 Account Balance

**Customer:** {data['customer']}

**Account Number:** {data['account']}

**Available Balance:** {data['balance']}

**Status:** {data['status']}
"""
        except Exception as e:
            answer = f"Unable to connect to Banking API.\n\n{e}"

    # FASTAPI - IFSC #

    elif "ifsc" in question:
        st.info("Calling IFSC Service...")
        try:
            response = requests.get(f"{API_URL}/ifsc")
            response.raise_for_status()
            data = response.json()
            answer = f"""
## 🏦 IFSC Information

**Bank:** {data['bank']}

**IFSC Code:** {data['ifsc']}
"""
        except Exception as e:
            answer = f"Unable to retrieve IFSC.\n\n{e}"

    # ==========================================================
    # FASTAPI - Branch
    # ==========================================================

    elif "branch" in question:
        st.info("Calling Branch Service...")
        try:
            response = requests.get(f"{API_URL}/branch")
            response.raise_for_status()
            data = response.json()
            answer = f"""
##  Branch Details

**Branch:** {data['branch']}

**Working Hours:** {data['timing']}
"""
        except Exception as e:
            answer = f"Unable to retrieve branch information.\n\n{e}"

    # FASTAPI - Loan

    elif (
        "loan details" in question
        or "interest rate" in question
        or "loan amount" in question
    ):
        st.info("🔧 Calling Loan Service...")
        try:
            response = requests.get(f"{API_URL}/loan")
            response.raise_for_status()
            data = response.json()
            answer = f"""
## 🏠 Home Loan

**Loan Type:** {data['loan_type']}

**Interest Rate:** {data['interest_rate']}

**Maximum Amount:** {data['max_amount']}
"""
        except Exception as e:
            answer = f"❌ Unable to retrieve loan details.\n\n{e}"

    # RAG (PDF Search)

    elif is_rag_query:
        st.info("📄 Searching Enterprise Knowledge Base...")
        try:
            with st.spinner("Searching PDF documents..."):
                context, sources = search_documents(prompt)

                response = chat(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": f"""
You are an Enterprise Banking AI Assistant.

Answer ONLY from the supplied banking documents.

Context:

{context}

If the answer cannot be found in the documents,
reply politely that the information is unavailable.
"""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                answer = response["message"]["content"]

        except Exception as e:
            answer = f"RAG Search Error\n\n{e}"

    # General AI (Ollama)

    else:
        st.info("🤖 Using Ollama LLM...")
        try:
            with st.spinner("Thinking..."):
                response = chat(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are an Enterprise Banking AI Assistant.

Answer professionally.

Keep answers concise.

Use bullet points whenever possible.

If you don't know the answer,
say you don't know.
"""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                answer = response["message"]["content"]

        except Exception as e:
            answer = f"Ollama Error\n\n{e}"

    # Display Assistant Response #

    answer_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    with st.chat_message("assistant"):
        st.markdown(body=answer)

        # Show retrieved documents only for RAG queries
        if is_rag_query:
            st.markdown(body=answer)

            if sources:
                render_source_downloads(sources, key_prefix=f"new_{answer_timestamp}")

            st.success("📄 Source : Enterprise Banking Knowledge Base (RAG)")

        elif is_api_query:
            st.success(" Source : Enterprise Banking REST API (FastAPI)")

        else:
            st.success(f"🤖 Source : Ollama ({MODEL_NAME})")

        st.caption(
            f"🕒 Generated at {datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')}"
        )

        st.download_button(
            label="⬇️ Download this answer",
            data=answer,
            file_name=f"banking_answer_{answer_timestamp}.md",
            mime="text/markdown",
            key=f"download_new_{answer_timestamp}"
        )

    # Save Assistant Response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "timestamp": answer_timestamp,
            "sources": sources if is_rag_query else []
        }
    )