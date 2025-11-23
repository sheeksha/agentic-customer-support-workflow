import json
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from langchain_core.documents import Document

from .llm_client import get_embeddings

BASE_DIR = Path(__file__).resolve().parents[2]  # go up from services -> app -> root
KB_PATH = BASE_DIR / "data" / "kb_articles.json"


class KnowledgeBase:
    """
    Simple in-memory knowledge base with numpy-based cosine similarity search.
    No FAISS or external vector DB needed.
    """

    def __init__(self):
        self.embeddings_model = get_embeddings()
        self.documents: List[Document] = []
        self.doc_vectors: np.ndarray | None = None
        self._load_and_build_index()

    def _load_and_build_index(self):
        with open(KB_PATH, "r", encoding="utf-8") as f:
            kb_data = json.load(f)

        docs: List[Document] = []
        for item in kb_data:
            content = item["content"]
            metadata = {
                "id": item["id"],
                "title": item["title"],
                "category": item.get("category"),
                "tags": item.get("tags", []),
            }
            docs.append(Document(page_content=content, metadata=metadata))

        self.documents = docs

        # Compute embeddings for all documents once
        texts = [d.page_content for d in docs]
        if texts:
            vectors = self.embeddings_model.embed_documents(texts)
            self.doc_vectors = np.array(vectors, dtype="float32")
        else:
            self.doc_vectors = np.zeros((0, 768), dtype="float32")  # safe default

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Return top-k most similar documents to the query using cosine similarity.
        """
        if self.doc_vectors is None or len(self.doc_vectors) == 0:
            return []

        query_vec = np.array(self.embeddings_model.embed_query(query), dtype="float32")

        # cosine similarity: (A·B) / (|A||B|)
        doc_norms = np.linalg.norm(self.doc_vectors, axis=1) + 1e-8
        query_norm = np.linalg.norm(query_vec) + 1e-8
        sims = (self.doc_vectors @ query_vec) / (doc_norms * query_norm)

        # get indices of top-k similarities
        top_k_idx = np.argsort(sims)[::-1][:k]

        results: List[Dict[str, Any]] = []
        for idx in top_k_idx:
            doc = self.documents[idx]
            results.append(
                {
                    "content": doc.page_content,
                    "title": doc.metadata.get("title"),
                    "category": doc.metadata.get("category"),
                    "tags": doc.metadata.get("tags"),
                    "id": doc.metadata.get("id"),
                }
            )

        return results


# simple singleton-style instance
kb = KnowledgeBase()
