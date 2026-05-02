import os
import requests
from collections import Counter
import re
from dotenv import load_dotenv

load_dotenv()

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_search_query(paper_names, max_words=12):
    text = " ".join(paper_names)
    text = text.replace(".pdf", "").replace("_", " ").replace("-", " ")
    words = re.findall(r"[A-Za-z]{4,}", text.lower())

    stopwords = {
        "paper", "research", "final", "draft", "review",
        "study", "based", "using", "with", "from"
    }

    keywords = [w for w in words if w not in stopwords]
    most_common = [w for w, _ in Counter(keywords).most_common(max_words)]

    return " ".join(most_common)


def recommend_related_papers(paper_names, limit=10):
    query = build_search_query(paper_names)

    if not query:
        query = "retrieval augmented generation research papers"

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,citationCount,venue"
    }

    headers = {
        "User-Agent": "ResearchPaperIntelligence/1.0"
    }

    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key

    response = requests.get(
        SEMANTIC_SCHOLAR_URL,
        params=params,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    papers = response.json().get("data", [])

    results = []
    for paper in papers:
        authors = paper.get("authors", [])
        author_names = ", ".join(a.get("name", "") for a in authors[:3])

        results.append({
            "title": paper.get("title", "Unknown title"),
            "authors": author_names,
            "year": paper.get("year", "Unknown"),
            "venue": paper.get("venue", "Unknown"),
            "citations": paper.get("citationCount", 0),
            "abstract": paper.get("abstract", "No abstract available."),
            "url": paper.get("url", "")
        })

    return query, results