from langchain_core.messages import SystemMessage, HumanMessage

from app.services.llm_client import get_llm
from app.models.schemas import DraftResponse, FinalResponse


def improve_response_style(draft: DraftResponse) -> FinalResponse:
    """
    Reviews and improves the draft response, focusing on tone, clarity, and professionalism.
    """
    llm = get_llm()

    system_prompt = (
        "You are a senior customer support quality reviewer. "
        "You will receive a draft reply to a customer.\n"
        "Improve it for clarity, politeness, empathy, and professionalism. "
        "Keep the meaning the same. Fix grammar and structure.\n"
        "Return only the improved reply text, no explanations."
    )

    user_prompt = f"Draft reply:\n{draft.draft_text}"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)
    final_text = response.content


    return FinalResponse(final_text=final_text.strip())
