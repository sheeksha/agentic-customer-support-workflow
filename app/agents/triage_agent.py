import json
from typing import Dict, Any

from langchain_core.messages import SystemMessage, HumanMessage


from app.services.llm_client import get_llm
from app.models.schemas import TriageResult


def classify_ticket(ticket_text: str) -> TriageResult:
    """
    Uses LLM to classify the incoming ticket into category, priority and sentiment.
    Returns a TriageResult Pydantic model.
    """
    llm = get_llm()

    system_prompt = (
        "You are a customer support triage assistant. "
        "You will receive a support ticket message and must classify it.\n\n"
        "Return a JSON object with the following fields:\n"
        "- category: one of [authentication, billing, account, performance, features, general]\n"
        "- priority: one of [low, medium, high, urgent]\n"
        "- sentiment: short description (e.g., calm, frustrated, angry, confused)\n"
        "- notes: short explanation of your reasoning."
    )

    user_prompt = f"Support ticket message:\n```{ticket_text}```"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)
    raw = response.content

    # we expect JSON, but be defensive
    try:
        data: Dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError:
        # fallback: naive parsing
        data = {
            "category": "general",
            "priority": "medium",
            "sentiment": "unknown",
            "notes": f"Failed to parse JSON. Raw output: {raw}",
        }

    return TriageResult(
        category=data.get("category", "general"),
        priority=data.get("priority", "medium"),
        sentiment=data.get("sentiment"),
        notes=data.get("notes"),
    )
