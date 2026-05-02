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
---

## 🛠️ Installation

### 1. Clone the repository

git clone https://github.com/sapna-baniya/Research_paper_intelligence.git

Research_paper_intelligence

---


### 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
3. Upgrade pip (recommended)
pip install --upgrade pip

---

###4. Install dependencies
All required libraries are listed in requirements.txt.
pip install -r requirements.txt

---

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

Run the following command to start the system:

python3 -m streamlit run app.py

🧪 How to Use
Step 1: Upload Papers

Upload one or more PDF files and click Process Papers.

Step 2: Configure System

Choose an LLM:
• Ollama
• Gemini
• Groq

Adjust parameters:
• Top-K retrieval
• Chunk size
• Chunk overlap

Step 3: Use Features
💬 Chat

Ask questions such as:
• What datasets are used in these papers?
• Compare the methods used
• What are the key contributions?

📊 Compare

Enter a comparison query.

Example:
Compare methods and results across papers

---
---
⚡ Quick Analysis
• Summarize all papers
• Extract datasets
• Identify best-performing paper
---
📋 Comparison Table
• Generate a structured comparison table
• Download results as CSV
---
🔍 Related Papers
• Fetch external research using Semantic Scholar
• View title, authors, abstract, and citations
---
🧠 System Pipeline
PDF → Text Extraction → Text Chunking → Embedding → Vector Storage → Retrieval → LLM Generation → External Recommendation
---
📦 Requirements
Key dependencies include:
• streamlit
• langchain
• chromadb
• sentence-transformers
• transformers
• torch
• pymupdf
• requests
(All dependencies are managed via requirements.txt)
---
⚠️ Notes
• Ollama must be running for local model:
ollama run llama3
---
• Internet connection is required for:
– Gemini
– Groq
– Semantic Scholar API
---
🧪 Example Use Cases
• Research paper summarization
• Literature comparison
• Dataset extraction
• Performance evaluation
• Finding related academic work
---
📌 Limitations
• Performance depends on retrieval quality
• Chunking strategy affects accuracy
• External APIs may introduce latency
• Local models depend on hardware
---
🔮 Future Improvements
• Add quantitative evaluation metrics
• Improve retrieval with re-ranking
• Model routing based on query type
• Better UI visualization
• Citation-aware responses
---
👨‍💻 Authors
Dipa Khadka
Sapna Baniya
---
📄 License
This project is for academic use.
---