import json

with open("data/tickets_sample.json", "r", encoding="utf-8") as f:
    tickets = json.load(f)

with open("data/kb_articles.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

print(len(tickets), "tickets loaded")
print(len(kb), "kb articles loaded")
