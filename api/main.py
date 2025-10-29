from bot.schemas.ticket import Ticket
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
def ticket(payload: Ticket):
    data = payload.model_dump()
    # einfache Speicherung für Demo
    import os, json, uuid
    os.makedirs("reports", exist_ok=True)
    data["id"] = str(uuid.uuid4())
    with open("reports/ticket_payload.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"ok": True, "ticket": data}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    # einfache statische Version; später aus git ableiten
    return {"name": "allO AI Support Agent Prototype", "version": "0.1.0"}

