import json
from datetime import datetime, timedelta
import random

subjects = [
    "Can't log into my account",
    "Billing charge looks wrong",
    "App keeps crashing on startup",
    "Requesting account cancellation",
    "Password reset email not received",
    "Change payment method",
    "Feature not working as expected",
    "Need invoice for last year",
    "Slow performance on dashboard",
    "Question about my subscription"
]

messages = [
    "Hi, I haven't been able to log into my account since this morning. It keeps saying my password is incorrect.",
    "Hello, I was charged twice for my subscription this month. Can you please check and refund the extra payment?",
    "Every time I open the mobile app, it crashes after a few seconds on my phone.",
    "I'd like to cancel my account at the end of this billing cycle. Please confirm when it's done.",
    "I tried resetting my password but I never receive the reset email, even in my spam folder.",
    "I want to update the credit card on my account but the payment page keeps showing an error.",
    "The export to CSV feature only downloads part of my data. Is there a limit on the number of records?",
    "I need all invoices for my account for the last year. How can I download them?",
    "The dashboard is extremely slow to load my reports compared to a few weeks ago.",
    "I have a question about what is included in my current subscription plan."
]

channels = ["email", "web", "chat"]
names = ["John Smith", "Sarah Lee", "Michael Brown", "Emily Davis", "David Johnson",
         "Olivia Wilson", "Daniel Martinez", "Sophia Garcia", "James Anderson", "Emma Thompson"]

base_time = datetime(2025, 11, 1, 9, 0, 0)

tickets = []
for i in range(1, 41):
    delta = timedelta(hours=random.randint(0, 240))
    created_at = (base_time + delta).isoformat() + "Z"
    idx = random.randint(0, len(subjects) - 1)
    tickets.append({
        "id": i,
        "channel": random.choice(channels),
        "customer_name": random.choice(names),
        "subject": subjects[idx],
        "message": messages[idx],
        "created_at": created_at
    })

with open("data/tickets_sample.json", "w", encoding="utf-8") as f:
    json.dump(tickets, f, indent=2)
