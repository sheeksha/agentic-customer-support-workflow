from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import TicketInput, WorkflowResult
from app.services.workflow import process_ticket_workflow

app = FastAPI(title="Agentic Customer Support Workflow")

# Allow frontend (Netlify/Vercel/localhost) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/process", response_model=WorkflowResult)
async def process_ticket(request: TicketInput):
    """
    Run the full multi-agent workflow on a single support ticket.

    Request: TicketInput (subject + message (+ optional channel/customer_name))
    Response: WorkflowResult (triage + retrieved_articles + draft + final)
    """
    try:
        ticket_dict = {
            "id": 0,
            "channel": request.channel,
            "customer_name": request.customer_name,
            "subject": request.subject,
            "message": request.message,
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        result = process_ticket_workflow(ticket_dict)
        return result
    except Exception as e:
        # You can log the error here if you add logging_utils later
        raise HTTPException(status_code=500, detail=str(e))