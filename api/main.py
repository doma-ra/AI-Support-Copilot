
from fastapi import FastAPI
from pydantic import BaseModel
from bot.router.support_router import handle_query

app = FastAPI(title="allO AI Support Agent Prototype")

class AskIn(BaseModel):
    query: str
    profile: str = "gastro"

@app.post("/ask")
def ask(payload: AskIn):
    return handle_query(payload.query, payload.profile)

class TicketIn(BaseModel):
    title: str
    description: str
    profile: str = "gastro"

@app.post("/ticket")
def ticket(payload: TicketIn):
    return {"ok": True, "payload": payload.model_dump()}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    # einfache statische Version; später aus git ableiten
    return {"name": "allO AI Support Agent Prototype", "version": "0.1.0"}

