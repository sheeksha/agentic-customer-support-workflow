import json
from pathlib import Path
from typing import List, Dict, Any

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


from .llm_client import get_embeddings

BASE_DIR = Path(__file__).resolve().parents[2]  # go up from services -> app -> root
KB_PATH = BASE_DIR / "data" / "kb_articles.json"


class KnowledgeBase:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.vector_store = None
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

        self.vector_store = FAISS.from_documents(docs, self.embeddings)

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        if self.vector_store is None:
            return []

        results = self.vector_store.similarity_search(query, k=k)
        formatted = []
        for doc in results:
            formatted.append(
                {
                    "content": doc.page_content,
                    "title": doc.metadata.get("title"),
                    "category": doc.metadata.get("category"),
                    "tags": doc.metadata.get("tags"),
                    "id": doc.metadata.get("id"),
                }
            )
        return formatted


# simple singleton-style instance
kb = KnowledgeBase()
