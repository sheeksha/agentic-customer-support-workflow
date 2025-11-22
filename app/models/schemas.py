from typing import List, Optional
from pydantic import BaseModel


class Ticket(BaseModel):
    id: int
    channel: str
    customer_name: str
    subject: str
    message: str
    created_at: str


class TriageResult(BaseModel):
    category: str
    priority: str
    sentiment: Optional[str] = None
    notes: Optional[str] = None


class RetrievedArticle(BaseModel):
    id: int
    title: str
    category: Optional[str] = None
    content: str
    tags: List[str] = []


class DraftResponse(BaseModel):
    draft_text: str


class FinalResponse(BaseModel):
    final_text: str


class WorkflowResult(BaseModel):
    triage: TriageResult
    retrieved_articles: List[RetrievedArticle]
    draft: DraftResponse
    final: FinalResponse
