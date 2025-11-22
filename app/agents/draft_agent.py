from typing import List
from langchain_core.messages import SystemMessage, HumanMessage


from app.services.llm_client import get_llm
from app.models.schemas import TriageResult, RetrievedArticle, DraftResponse


def generate_draft_response(
    ticket_text: str,
    triage: TriageResult,
    articles: List[RetrievedArticle],
) -> DraftResponse:
    llm = get_llm()

    kb_snippets = "\n\n".join(
        [
            f"Title: {a.title}\nContent: {a.content}"
            for a in articles
        ]
    ) or "No relevant knowledge base articles found."

    system_prompt = (
        "You are a professional customer support agent. "
        "You will receive a user ticket, triage information, and relevant knowledge base snippets. "
        "Write a clear, friendly, and concise reply that solves the issue or requests the minimum information needed.\n\n"
        "Do NOT mention that you are using an AI model or agents. "
        "Write in a helpful, human tone."
    )

    triage_text = (
        f"Category: {triage.category}\n"
        f"Priority: {triage.priority}\n"
        f"Sentiment: {triage.sentiment}\n"
        f"Notes: {triage.notes}"
    )

    user_prompt = (
        f"Support ticket:\n{ticket_text}\n\n"
        f"Triage information:\n{triage_text}\n\n"
        f"Knowledge base snippets:\n{kb_snippets}\n\n"
        "Now draft the reply to the customer."
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)
    draft_text = response.content


    return DraftResponse(draft_text=draft_text.strip())
