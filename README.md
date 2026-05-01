# 📚 Research Paper Intelligence System — User Guide

## 🧠 Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline for analyzing and interacting with research papers. The system allows users to upload PDF documents, extract knowledge, compare multiple papers, and generate responses using different Large Language Models (LLMs).

The system also integrates external research retrieval using the Semantic Scholar API.

---

## 🚀 Features

- 📄 Upload and process multiple research papers (PDF)
- 💬 Chat with documents using RAG
- 📊 Cross-paper comparison
- 📋 Structured comparison table generation
- ⚡ Multi-LLM support:
  - Ollama (local)
  - Gemini (Google)
  - Groq (fast inference)
- 🔍 External paper recommendation (Semantic Scholar)

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sapna-baniya/Research_paper_intelligence.git

cd Research_paper_intelligence

2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
3. Upgrade pip (recommended)
pip install --upgrade pip

4. Install dependencies
All required libraries are listed in requirements.txt.
pip install -r requirements.txt

5. (Optional) Install Ollama for local LLM
Download from:
👉 https://ollama.com/download

Then run:
ollama run llama3

6. Setup environment variables

Create a .env file in the root directory:

GOOGLE_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
SEMANTIC_SCHOLAR_API_KEY=your_key

⚠️ Do NOT upload .env to GitHub.

▶️ Running the Application
python3 -m streamlit run app.py
🧪 How to Use
Step 1: Upload Papers
Upload one or more PDF files
Click Process Papers
Step 2: Configure System
Choose LLM:
Ollama
Gemini
Groq
Adjust:
Top-K retrieval
Chunk size
Chunk overlap

Step 3: Use Features
💬 Chat

Ask questions like:

What datasets are used in these papers?
Compare the methods used
What are the key contributions?
📊 Compare
Enter comparison query
Example:
Compare methods and results across papers
⚡ Quick Analysis
Summarize all papers
Extract datasets
Identify best-performing paper
📋 Comparison Table
Generate structured table
Download as CSV
🔍 Related Papers
Fetch external research using Semantic Scholar
View title, authors, abstract, citations
🧠 System Pipeline
PDF → Text Extraction (PyMuPDF)
Text Chunking (RecursiveCharacterTextSplitter)
Embedding (HuggingFace)
Vector Storage (ChromaDB)
Retrieval (Top-K similarity)
Generation (LLM)
External Recommendation (Semantic Scholar API)
📦 Requirements

Key dependencies include:

streamlit
langchain
chromadb
sentence-transformers
transformers
torch
pymupdf
requests

All dependencies are managed via requirements.txt.

⚠️ Notes
Ollama must be running for local model:
ollama run llama3
Internet required for:
Gemini
Groq
Semantic Scholar API
Do NOT commit .env file
🧪 Example Use Cases
Research paper summarization
Literature comparison
Dataset extraction
Performance evaluation
Finding related academic work
📌 Limitations
Performance depends on retrieval quality
Chunking strategy affects accuracy
External APIs may introduce latency
Local models depend on hardware
🔮 Future Improvements
Add quantitative evaluation metrics
Improve retrieval with re-ranking
Model routing based on query type
Better UI visualization
Citation-aware responses

👨‍💻 Authors
Dipa Khadka
Sapna Baniya

📄 License
This project is for academic use.