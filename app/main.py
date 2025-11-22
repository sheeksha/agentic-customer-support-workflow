from fastapi import FastAPI

app = FastAPI(title="Agentic Customer Support Workflow")

@app.get("/health")
def health_check():
    return {"status": "ok"}
