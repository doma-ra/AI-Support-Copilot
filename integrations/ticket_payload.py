from datetime import datetime
from typing import Dict
from bot.schema import BotResponse

REQUIRED = ["source","customer","summary","intent","severity","escalate"]

def build_ticket(resp: BotResponse, *, source: str, customer: str, query: str) -> Dict:
    """Konvertiert BotResponse in ein Jira/Zendesk-ähnliches Payload."""
    payload = {
        "created_at": datetime.utcnow().isoformat() + "Z",
        "source": source,
        "customer": customer,
        "summary": f"[{resp.intent}/{resp.severity}] {query[:120]}",
        "intent": resp.intent,
        "severity": resp.severity,
        "answer": resp.answer,
        "kb_refs": resp.kb_refs,
        "escalate": resp.escalate,
        "handoff_note": resp.handoff_note,
        "faq_id": resp.faq_id,
        # rudimentäre Felder für L2
        "steps_to_reproduce": [],
        "expected": "",
        "actual": query,
        "next_action": ("Follow KB" if resp.kb_refs else "Investigate/L2"),
    }
    # Minimalvalidierung
    for k in REQUIRED:
        if payload.get(k) in (None, ""):
            raise ValueError(f"ticket missing field: {k}")
    return payload

