from typing import List

from app.services.knowledge_base import kb
from app.models.schemas import RetrievedArticle


def retrieve_relevant_articles(query: str, k: int = 3) -> List[RetrievedArticle]:
    """
    Uses the knowledge base to find the most relevant KB articles for the ticket.
    """
    results = kb.search(query, k=k)

    articles: List[RetrievedArticle] = []
    for item in results:
        articles.append(
            RetrievedArticle(
                id=item["id"],
                title=item["title"],
                category=item.get("category"),
                content=item["content"],
                tags=item.get("tags") or [],
            )
        )

    return articles
