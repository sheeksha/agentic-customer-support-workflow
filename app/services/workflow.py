from typing import Dict, Any

from app.models.schemas import (
    Ticket,
    WorkflowResult,
)
from app.agents.triage_agent import classify_ticket
from app.agents.retrieval_agent import retrieve_relevant_articles
from app.agents.draft_agent import generate_draft_response
from app.agents.qa_agent import improve_response_style


def process_ticket_workflow(ticket_data: Dict[str, Any]) -> WorkflowResult:
    """
    Main workflow: Triage -> Retrieval -> Draft -> QA.
    ticket_data is typically a dict parsed from request.
    """
    ticket = Ticket(**ticket_data)

    # 1. Triage
    triage = classify_ticket(ticket.message)

    # 2. Retrieval
    articles = retrieve_relevant_articles(ticket.message, k=3)

    # 3. Draft
    draft = generate_draft_response(ticket.message, triage, articles)

    # 4. QA
    final = improve_response_style(draft)

    return WorkflowResult(
        triage=triage,
        retrieved_articles=articles,
        draft=draft,
        final=final,
    )
