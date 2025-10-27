import os
import json
from typing import Tuple
from dotenv import load_dotenv
from .inference import validate_raw

load_dotenv()
PROVIDER = os.getenv("MODEL_PROVIDER", "mock").lower()

def _call_provider(query: str) -> str:
    """
    Platzhalter für echte Modellaufrufe.
    'mock' liefert bewusst schon valides JSON (v2-Stil).
    Später: OPENAI/… hier einhängen.
    """
    if PROVIDER == "mock":
        return json.dumps({
            "intent": "other",
            "severity": "medium",
            "answer": "Kein FAQ/KB-Treffer. Eskaliere mit klaren Notizen.",
            "actions": [],
            "kb_refs": [],
            "escalate": True,
            "handoff_note": "Bitte Logs, Zeit, Gerät, Kassenversion anhängen.",
            "faq_id": None
        })
    # Platz für echte Provider:
    # return openai_response_text
    return "{}"  # absichtlich kaputt als Worst-Case

def _repair(_: str) -> str:
    """
    Minimaler Repair-Schritt: erzeuge ein garantiert gültiges Fallback-JSON.
    """
    return json.dumps({
        "intent": "other",
        "severity": "medium",
        "answer": "Reparierter Fallback.",
        "actions": [],
        "kb_refs": [],
        "escalate": True,
        "handoff_note": "Bitte Logs/Zeiten/Schritte ergänzen.",
        "faq_id": None
    })

def generate_v2(query: str):
    """
    v2 Prompt-Pfad: ruft Provider, validiert strikt, repariert bei Bedarf.
    Liefert (ok, BotResponse | Fehlertext).
    """
    raw = _call_provider(query)
    ok, res = validate_raw(raw)
    if ok:
        return ok, res
    # 1. Repair
    raw2 = _repair(raw)
    ok2, res2 = validate_raw(raw2)
    if ok2:
        return ok2, res2
    # 2. Harte Fallback-Garantie
    raw3 = _repair("{}")
    ok3, res3 = validate_raw(raw3)
    return ok3, res3
