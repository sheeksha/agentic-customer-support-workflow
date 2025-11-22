import json
from pathlib import Path

from app.services.workflow import process_ticket_workflow

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "data" / "tickets_sample.json", "r", encoding="utf-8") as f:
    tickets = json.load(f)

sample_ticket = tickets[0]

result = process_ticket_workflow(sample_ticket)

print("TRIAGE:", result.triage)
print("\nARTICLES:")
for a in result.retrieved_articles:
    print("-", a.title)

print("\nDRAFT:\n", result.draft.draft_text)
print("\nFINAL:\n", result.final.final_text)
