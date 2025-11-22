# Agentic Workflow for Customer Support Automation

This project implements a multi-agent LLM-powered workflow to automate customer support ticket handling.

## Architecture

1. **Triage Agent**  
   Classifies the incoming ticket (category, priority, sentiment).

2. **Retrieval Agent**  
   Searches the internal knowledge base (FAQ / articles) using semantic search.

3. **Draft Response Agent**  
   Generates a first response draft using LLM + retrieved context.

4. **QA Agent**  
   Reviews the draft for tone, correctness, and clarity, and outputs the final response.

## Tech Stack

- Python, FastAPI
- LangChain + OpenAI (LLM + agents)
- FAISS for vector search
- Simple frontend (to be added) for demo
