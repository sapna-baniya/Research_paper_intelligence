import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from src.pdf_loader import extract_text_from_pdf
from src.chunker import chunk_pages
from src.vector_store import create_vector_store
from src.rag_pipeline import (
    answer_question,
    compare_papers,
    summarize_each_paper,
    generate_comparison_table
)
from src.compare import build_source_table, parse_comparison_json
from src.paper_recommender import recommend_related_papers

load_dotenv()

st.set_page_config(
    page_title="Research Paper Intelligence System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Premium UI CSS
# -------------------------------------------------
st.markdown("""
<style>
:root {
    --bg-1: #050816;
    --bg-2: #0b1020;
    --bg-3: #111827;
    --card: rgba(15, 23, 42, 0.72);
    --card-2: rgba(17, 24, 39, 0.78);
    --line: rgba(255,255,255,0.08);
    --text: #f8fafc;
    --muted: #94a3b8;
    --blue: #60a5fa;
    --violet: #8b5cf6;
    --cyan: #22d3ee;
    --shadow: 0 10px 30px rgba(0,0,0,0.28);
}

/* App background */
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(96,165,250,0.14), transparent 26%),
        radial-gradient(circle at 82% 18%, rgba(139,92,246,0.12), transparent 26%),
        radial-gradient(circle at 50% 78%, rgba(34,211,238,0.08), transparent 28%),
        linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 48%, var(--bg-3) 100%);
    color: var(--text);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.6rem;
    padding-bottom: 2rem;
}

#MainMenu, footer {
    visibility: hidden;
}

[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(7,11,24,0.96), rgba(15,23,42,0.96));
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}
.sidebar-brand {
    padding: 0.6rem 0 1rem 0;
}
.brand-badge {
    display: inline-block;
    padding: 0.3rem 0.7rem;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(96,165,250,0.15), rgba(139,92,246,0.15));
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 0.82rem;
    color: #dbeafe;
    margin-bottom: 0.75rem;
}
.brand-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 0.2rem;
}
.brand-sub {
    color: #94a3b8;
    font-size: 0.92rem;
    line-height: 1.45;
}

.hero-shell {
    position: relative;
    overflow: hidden;
    border-radius: 28px;
    border: 1px solid rgba(255,255,255,0.08);
    background:
        linear-gradient(135deg, rgba(15,23,42,0.84), rgba(17,24,39,0.80)),
        radial-gradient(circle at top left, rgba(96,165,250,0.14), transparent 30%);
    box-shadow: var(--shadow);
    padding: 32px 34px;
    margin-bottom: 22px;
}
.hero-shell::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        radial-gradient(circle at 18% 10%, rgba(96,165,250,0.14), transparent 20%),
        radial-gradient(circle at 78% 14%, rgba(139,92,246,0.15), transparent 20%),
        radial-gradient(circle at 60% 80%, rgba(34,211,238,0.08), transparent 20%);
    pointer-events: none;
}
.hero-eyebrow {
    display: inline-block;
    font-size: 0.85rem;
    color: #dbeafe;
    padding: 0.36rem 0.8rem;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    margin-bottom: 0.9rem;
}
.hero-title {
    font-size: 3rem;
    line-height: 1.02;
    font-weight: 900;
    margin-bottom: 0.7rem;
    letter-spacing: -0.03em;
    color: #f8fafc;
}
.hero-title .grad {
    background: linear-gradient(90deg, #93c5fd, #c4b5fd, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    max-width: 920px;
    color: #cbd5e1;
    font-size: 1.03rem;
    line-height: 1.7;
}
.hero-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-top: 18px;
}
.hero-pill {
    border-radius: 16px;
    padding: 12px 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    color: #dbeafe;
    font-size: 0.94rem;
}

.glass-card {
    background: rgba(15,23,42,0.64);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    box-shadow: var(--shadow);
    padding: 20px 22px;
    margin-bottom: 18px;
}
.subtle-card {
    background: rgba(17,24,39,0.72);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.22);
    padding: 16px 18px;
    margin-bottom: 16px;
}

.section-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 0.35rem;
}
.section-sub {
    font-size: 0.95rem;
    color: #94a3b8;
    margin-bottom: 0.8rem;
}

.metric-wrap {
    background: linear-gradient(180deg, rgba(17,24,39,0.92), rgba(15,23,42,0.92));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.22);
}
.metric-label {
    color: #93a3b8;
    font-size: 0.92rem;
    margin-bottom: 0.45rem;
}
.metric-value {
    color: #ffffff;
    font-size: 2.1rem;
    font-weight: 900;
    letter-spacing: -0.02em;
}

.stButton > button {
    width: 100%;
    border: none;
    border-radius: 16px;
    padding: 0.78rem 1.1rem;
    font-weight: 800;
    color: white !important;
    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 55%, #06b6d4 100%);
    box-shadow: 0 10px 24px rgba(37,99,235,0.24);
    transition: all 0.18s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.06);
}
.stDownloadButton > button {
    width: 100%;
    border: none;
    border-radius: 16px;
    padding: 0.78rem 1.1rem;
    font-weight: 800;
    color: white !important;
    background: linear-gradient(135deg, #0f766e 0%, #0891b2 100%);
    box-shadow: 0 10px 24px rgba(8,145,178,0.22);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    margin-bottom: 14px;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.04);
    color: #cbd5e1;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.05);
    padding: 11px 16px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(37,99,235,0.20), rgba(139,92,246,0.20));
    color: white !important;
    border: 1px solid rgba(96,165,250,0.35);
    box-shadow: 0 6px 18px rgba(59,130,246,0.12);
}

.stTextInput > div > div > input,
.stTextArea textarea,
[data-testid="stFileUploader"] section,
[data-testid="stChatInput"] textarea {
    background: rgba(15,23,42,0.9) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
}
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03);
    border-radius: 18px;
    border: 1px dashed rgba(255,255,255,0.13);
    padding: 0.45rem;
}
[data-testid="stChatInput"] {
    position: sticky;
    bottom: 0;
    padding-top: 0.6rem;
    background: linear-gradient(180deg, rgba(5,8,22,0.0), rgba(5,8,22,0.96) 40%);
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 0.8rem;
    box-shadow: 0 8px 18px rgba(0,0,0,0.14);
}
.chat-note {
    color: #94a3b8;
    font-size: 0.92rem;
    margin-bottom: 0.6rem;
}

.streamlit-expanderHeader {
    background: rgba(15,23,42,0.84);
    border-radius: 14px;
}

.stAlert {
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.07);
}

.footer-card {
    margin-top: 22px;
    border-radius: 22px;
    background: rgba(17,24,39,0.58);
    border: 1px solid rgba(255,255,255,0.07);
    padding: 16px 18px;
    color: #94a3b8;
    font-size: 0.92rem;
    text-align: center;
}

@media (max-width: 900px) {
    .hero-title {
        font-size: 2.2rem;
    }
    .hero-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = None
if "papers_processed" not in st.session_state:
    st.session_state["papers_processed"] = False
if "paper_names" not in st.session_state:
    st.session_state["paper_names"] = []
if "total_chunks" not in st.session_state:
    st.session_state["total_chunks"] = 0
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-badge">AI Research Workspace</div>
        <div class="brand-title">Research Intelligence</div>
        <div class="brand-sub">
            Upload papers, retrieve grounded evidence, compare findings,
            and interact with your academic corpus in a premium interface.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Configuration")
    top_k = st.slider("Retrieved chunks (Top-K)", 2, 20, 10)
    chunk_size = st.slider("Chunk size", 500, 1500, 1000, 100)
    chunk_overlap = st.slider("Chunk overlap", 50, 400, 200, 50)

    # NEW: LLM selector
    model_choice = st.selectbox(
        "Choose LLM",
        ["ollama", "gemini", "groq"]
    )

    st.markdown("---")
    st.markdown("### Suggested Prompts")
    st.markdown("""
- Summarize each uploaded paper  
- Compare the methods across the papers  
- What datasets are mentioned?  
- Which paper reports the best performance?  
- Extract the evaluation metrics  
- What limitations are identified?  
""")

    st.markdown("---")
    st.caption("Built for academic RAG and multi-paper analysis.")

# -------------------------------------------------
# Hero
# -------------------------------------------------
st.markdown("""
<div class="hero-shell">
    <div class="hero-eyebrow">Academic RAG • Multi-Paper Analysis • Chat Interface</div>
    <div class="hero-title">
        Research Paper <span class="grad">Intelligence System</span>
    </div>
    <div class="hero-sub">
        A premium AI-powered workspace for academic research. Upload research papers,
        chat across multiple documents, compare methods and results, extract structured
        knowledge, and generate grounded answers with evidence from the source papers.
    </div>
    <div class="hero-grid">
        <div class="hero-pill">📄 Multi-PDF ingestion and semantic indexing</div>
        <div class="hero-pill">💬 Conversational question answering over papers</div>
        <div class="hero-pill">📊 Structured comparison and extraction workflows</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def process_uploaded_papers(files):
    all_chunks = []
    paper_names = []

    for uploaded_file in files:
        paper_names.append(uploaded_file.name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file.read())
            temp_pdf_path = temp_pdf.name

        try:
            pages = extract_text_from_pdf(temp_pdf_path, uploaded_file.name)
            chunks = chunk_pages(
                pages=pages,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            all_chunks.extend(chunks)
        finally:
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)

    return all_chunks, paper_names


def reset_processed_state():
    st.session_state["vector_store"] = None
    st.session_state["papers_processed"] = False
    st.session_state["paper_names"] = []
    st.session_state["total_chunks"] = 0
    st.session_state["chat_history"] = []

# -------------------------------------------------
# Upload Section
# -------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📂 Upload Research Papers</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Add one or more PDF papers to build your research knowledge base.</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload research papers (PDF only)",
    type=["pdf"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    st.info(f"{len(uploaded_files)} file(s) uploaded and ready for processing.")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("🚀 Process Papers"):
            with st.spinner("Extracting text, chunking, embedding, and indexing papers..."):
                try:
                    all_chunks, paper_names = process_uploaded_papers(uploaded_files)

                    if not all_chunks:
                        st.error("No readable text could be extracted from the uploaded PDFs.")
                    else:
                        vector_store = create_vector_store(all_chunks)
                        st.session_state["vector_store"] = vector_store
                        st.session_state["papers_processed"] = True
                        st.session_state["paper_names"] = paper_names
                        st.session_state["total_chunks"] = len(all_chunks)
                        st.session_state["chat_history"] = []
                        st.success("Papers processed successfully.")
                except Exception as e:
                    st.error(f"Processing error: {str(e)}")

    with col_b:
        if st.button("♻ Reset Workspace"):
            reset_processed_state()
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# Stats
# -------------------------------------------------
if st.session_state["papers_processed"]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Workspace Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Your uploaded paper collection is indexed and ready.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-wrap">
            <div class="metric-label">Number of Papers</div>
            <div class="metric-value">{len(st.session_state["paper_names"])}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-wrap">
            <div class="metric-label">Total Chunks</div>
            <div class="metric-value">{st.session_state["total_chunks"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("View Uploaded Paper Names"):
        for name in st.session_state["paper_names"]:
            st.write(f"- {name}")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# Main app area
# -------------------------------------------------
if st.session_state["papers_processed"] and st.session_state["vector_store"] is not None:
    tab1, tab2, tab3, tab4,tab5 = st.tabs([
        "💬 Chat",
        "📑 Compare",
        "⚡ Quick Analysis",
        "📋 Comparison Table",
        "🔍 Related Papers"

    ])

    # Chat tab
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💬 Chat with Your Papers</div>', unsafe_allow_html=True)
        st.markdown('<div class="chat-note">Ask multiple questions in sequence. The system will use recent conversation context where helpful.</div>', unsafe_allow_html=True)

        colx, coly = st.columns([1, 5])
        with colx:
            if st.button("Clear Chat"):
                st.session_state["chat_history"] = []
                st.rerun()

        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

                if msg["role"] == "assistant" and "sources" in msg:
                    with st.expander("View Sources"):
                        for i, doc in enumerate(msg["sources"], start=1):
                            paper_name = doc.metadata.get("paper_name", "Unknown")
                            page = doc.metadata.get("page", "Unknown")
                            chunk_id = doc.metadata.get("chunk_id", "Unknown")
                            st.write(f"**Source {i}:** {paper_name} | Page {page} | {chunk_id}")
                            st.write(doc.page_content)
                            st.markdown("---")

        user_question = st.chat_input("Ask a question about the uploaded papers")

        if user_question:
            st.session_state["chat_history"].append({
                "role": "user",
                "content": user_question
            })

            with st.chat_message("user"):
                st.markdown(user_question)

            with st.chat_message("assistant"):
                with st.spinner(f"Thinking with {model_choice}..."):
                    try:
                        result = answer_question(
                            st.session_state["vector_store"],
                            user_question,
                            chat_history=st.session_state["chat_history"],
                            per_paper=2,
                            total_k=max(top_k, 12),
                            model_name=model_choice
                        )

                        st.markdown(result["answer"])

                        retrieved_papers = sorted(
                            set(doc.metadata.get("paper_name", "Unknown") for doc in result["source_documents"])
                        )
                        st.markdown("**Retrieved Papers:**")
                        st.write(retrieved_papers)

                        with st.expander("View Sources"):
                            for i, doc in enumerate(result["source_documents"], start=1):
                                paper_name = doc.metadata.get("paper_name", "Unknown")
                                page = doc.metadata.get("page", "Unknown")
                                chunk_id = doc.metadata.get("chunk_id", "Unknown")
                                st.write(f"**Source {i}:** {paper_name} | Page {page} | {chunk_id}")
                                st.write(doc.page_content)
                                st.markdown("---")

                        st.session_state["chat_history"].append({
                            "role": "assistant",
                            "content": result["answer"],
                            "sources": result["source_documents"]
                        })

                    except Exception as e:
                        st.error(f"Answer generation error: {str(e)}")

        st.markdown("</div>", unsafe_allow_html=True)

    # Compare tab
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📑 Compare Papers</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Run targeted cross-paper analysis for methods, datasets, results, and limitations.</div>', unsafe_allow_html=True)

        comparison_request = st.text_input(
            "Enter comparison request",
            placeholder="Example: Compare the methods, datasets, and results in these papers"
        )

        if st.button("Run Comparison"):
            if not comparison_request.strip():
                st.warning("Please enter a comparison request.")
            else:
                with st.spinner(f"Comparing papers with {model_choice}..."):
                    try:
                        result = compare_papers(
                            st.session_state["vector_store"],
                            comparison_request,
                            chat_history=st.session_state["chat_history"],
                            per_paper=3,
                            total_k=max(top_k, 15),
                            model_name=model_choice
                        )

                        st.markdown("### Comparison Result")
                        st.write(result["comparison"])

                        retrieved_papers = sorted(
                            set(doc.metadata.get("paper_name", "Unknown") for doc in result["source_documents"])
                        )
                        st.markdown("### Retrieved Papers")
                        st.write(retrieved_papers)

                        st.markdown("### Comparison Sources")
                        source_df = build_source_table(result["source_documents"])
                        st.dataframe(source_df, use_container_width=True)

                    except Exception as e:
                        st.error(f"Comparison error: {str(e)}")

        st.markdown("</div>", unsafe_allow_html=True)

    # Quick Analysis tab
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚡ Quick Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Use ready-made actions for fast demos and testing.</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Summarize All Papers"):
                with st.spinner(f"Generating summary with {model_choice}..."):
                    try:
                        result = answer_question(
                            st.session_state["vector_store"],
                            "For each uploaded paper, summarize its objective, method, and main findings. Then provide a combined summary.",
                            chat_history=st.session_state["chat_history"],
                            per_paper=2,
                            total_k=max(top_k, 12),
                            model_name=model_choice
                        )
                        st.markdown("### Summary")
                        st.write(result["answer"])
                    except Exception as e:
                        st.error(f"Quick summary error: {str(e)}")

            if st.button("Extract Datasets"):
                with st.spinner(f"Extracting datasets with {model_choice}..."):
                    try:
                        result = answer_question(
                            st.session_state["vector_store"],
                            "List all datasets mentioned in the uploaded papers and state which paper uses each dataset.",
                            chat_history=st.session_state["chat_history"],
                            per_paper=2,
                            total_k=max(top_k, 12),
                            model_name=model_choice
                        )
                        st.markdown("### Datasets")
                        st.write(result["answer"])
                    except Exception as e:
                        st.error(f"Dataset extraction error: {str(e)}")

            if st.button("Summarize Each Paper"):
                with st.spinner(f"Summarizing each paper with {model_choice}..."):
                    try:
                        result = summarize_each_paper(
                            st.session_state["vector_store"],
                            st.session_state["paper_names"],
                            model_name=model_choice
                        )
                        st.markdown("### Paper-wise Summary")
                        st.write(result)
                    except Exception as e:
                        st.error(f"Paper-wise summary error: {str(e)}")

        with col2:
            if st.button("Extract Evaluation Metrics"):
                with st.spinner(f"Extracting metrics with {model_choice}..."):
                    try:
                        result = answer_question(
                            st.session_state["vector_store"],
                            "List the evaluation metrics mentioned in the uploaded papers and explain where they are used.",
                            chat_history=st.session_state["chat_history"],
                            per_paper=2,
                            total_k=max(top_k, 12),
                            model_name=model_choice
                        )
                        st.markdown("### Evaluation Metrics")
                        st.write(result["answer"])
                    except Exception as e:
                        st.error(f"Metric extraction error: {str(e)}")

            if st.button("Find Best Results"):
                with st.spinner(f"Finding best results with {model_choice}..."):
                    try:
                        result = answer_question(
                            st.session_state["vector_store"],
                            "Identify which uploaded paper reports the best performance and explain the reported results.",
                            chat_history=st.session_state["chat_history"],
                            per_paper=2,
                            total_k=max(top_k, 12),
                            model_name=model_choice
                        )
                        st.markdown("### Best Results")
                        st.write(result["answer"])
                    except Exception as e:
                        st.error(f"Best result extraction error: {str(e)}")

        st.markdown("</div>", unsafe_allow_html=True)

    # Comparison table tab
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 Structured Comparison Table</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Generate one structured row per uploaded paper and export it as CSV.</div>', unsafe_allow_html=True)

        if st.button("Generate Comparison Table"):
            with st.spinner(f"Building structured comparison table with {model_choice}..."):
                try:
                    result = generate_comparison_table(
                        st.session_state["vector_store"],
                        st.session_state["paper_names"],
                        per_paper=3,
                        total_k=max(top_k, 15),
                        model_name=model_choice
                    )

                    comparison_df = parse_comparison_json(result["table_json"])

                    st.markdown("### Comparison Table")
                    st.dataframe(comparison_df, use_container_width=True)

                    csv_data = comparison_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="Download Comparison Table as CSV",
                        data=csv_data,
                        file_name="paper_comparison_table.csv",
                        mime="text/csv"
                    )

                    retrieved_papers = sorted(
                        set(doc.metadata.get("paper_name", "Unknown") for doc in result["source_documents"])
                    )
                    st.markdown("### Retrieved Papers")
                    st.write(retrieved_papers)

                    st.markdown("### Extraction Sources")
                    source_df = build_source_table(result["source_documents"])
                    st.dataframe(source_df, use_container_width=True)

                    with st.expander("Show Raw LLM JSON Output"):
                        st.code(result["table_json"], language="json")

                except Exception as e:
                    st.error(f"Comparison table generation error: {str(e)}")

        st.markdown("</div>", unsafe_allow_html=True)
    with tab5:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔍 Related Paper Recommendations</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Find external research papers related to your uploaded PDFs using Semantic Scholar.</div>', unsafe_allow_html=True)

        if st.button("Find 10 Related Papers"):
            with st.spinner("Searching related papers..."):
                try:
                    paper_names = st.session_state.get("paper_names", [])

                    query, results = recommend_related_papers(paper_names)

                    st.markdown(f"### 🔎 Search Query")
                    st.write(query)

                    for paper in results:
                        st.markdown(f"""
                        <div class="glass-card">
                            <h4>{paper['title']}</h4>
                            <b>Authors:</b> {paper['authors']}<br>
                            <b>Year:</b> {paper['year']} | <b>Venue:</b> {paper['venue']}<br>
                            <b>Citations:</b> {paper['citations']}<br><br>
                            {paper['abstract']}<br><br>
                            <a href="{paper['url']}" target="_blank">📄 Read Paper</a>
                        </div>
                        """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Related paper search error: {str(e)}")

        st.markdown("</div>", unsafe_allow_html=True)
    

else:
    st.info("Upload PDFs and click 'Process Papers' to start.")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("""
<div class="footer-card">
    Research Paper Intelligence System • Premium academic RAG workspace • Multi-document retrieval, comparison, and evidence-grounded analysis
</div>
""", unsafe_allow_html=True)