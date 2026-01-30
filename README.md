# 🧠 Multisource Multimodal RAG Assistant

A full-stack Retrieval-Augmented Generation (RAG) system that ingests data from multiple sources — PDFs, images, websites, CSVs, DOCX, and text files — and answers user queries with **grounded, multimodal understanding** and **streaming AI responses**.

🚀 Built with FastAPI backend, Streamlit frontend, FAISS vector search, multimodal processing, and optional voice output.

---

## 📌 Features

### 🔍 What it can do  
- **📄 Ingest PDFs, TXT, DOCX, CSV** — text and structured data  
- **🖼️ Multimodal image handling** — captions + OCR pipeline support  
- **🌐 Web content ingestion** — fetches and indexes page content  
- **💡 Real-time streaming responses** to user queries  
- **📌 Source references** with page/row context  
- **🔊 Optional voice responses** for AI answers  
- **⚙️ FastAPI backend + Streamlit frontend** architecture

---

## 🧠 How RAG Works (Under the Hood)

1. **Chunking → Embeddings**  
   Source content is split into chunks and embedded with OpenAI embeddings.

2. **Vector Store (FAISS)**  
   Embeddings + metadata are stored in a FAISS vector database for fast semantic retrieval.

3. **Semantic Search**  
   User queries are embedded and matched to the most relevant chunks.

4. **Context-Augmented Generation**  
   Retrieved chunks are injected into an LLM prompt to produce grounded answers.

5. **Multimodal Fusion**  
   Image content is captioned and treated as text for unified retrieval.

---

## 📦 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend API | **FastAPI** |
| Frontend | **Streamlit** |
| Vector Search | **FAISS (local)** |
| LLM + Embeddings | **OpenAI GPT-4o & text-embedding-3-large** |
| Multimodal Processing | Vision + OCR (optional enhancements) |
| HTTP Client | **Requests** |

---

## 🔧 Getting Started

### 1. Clone Repo

```bash
git clone https://github.com/harshit-technocrat11/multisource-RAG-agent.git
cd multisource-RAG-agent
