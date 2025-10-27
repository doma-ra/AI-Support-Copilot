import csv
import re
from typing import Optional, Dict
from .schema import BotResponse

def load_faq(path: str) -> Dict[str, Dict[str, str]]:
    store = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            store[row["id"]] = {"q": row["question"], "a": row["answer"]}
    return store

_FAQ = None  # lazy load

def _ensure_loaded():
    global _FAQ
    if _FAQ is None:
        _FAQ = load_faq("data/faq.csv")

def route_faq(query: str) -> Optional[BotResponse]:
    """FAQ-Regeln; falls kein Treffer: KB-Retriever-Fallback."""
    _ensure_loaded()
    q = query.lower()

    # 1) Regex-Regeln für schnelle Treffer
    rules = [
        ("PAY-001", r"(kartenzahlung|karte|terminal).*fehl"),
        ("REC-001", r"(rechnung).*(neu|nochmal|erneut|drucken)"),
    ]
    for fid, pattern in rules:
        if re.search(pattern, q):
            ans = _FAQ[fid]["a"]
            return BotResponse(
                intent="payment" if fid.startswith("PAY") else "receipt",
                severity="medium",
                answer=ans,
                actions=[],
                kb_refs=[f"faq:{fid}"],
                escalate=False,
                handoff_note=None,
                faq_id=fid,
            )

    # 2) KB-Fallback
    from .retriever import retrieve_best  # lokal importieren, um Zyklen zu vermeiden
    hit = retrieve_best(query)
    if hit:
        intent = (
            "payment" if "payments" in hit["id"]
            else "receipt" if "receipt" in hit["id"]
            else "other"
        )
        return BotResponse(
            intent=intent,
            severity="medium",
            answer=f"Siehe KB: {hit['title']}",
            actions=[],
            kb_refs=[hit["id"]],
            escalate=False,
            handoff_note=None,
            faq_id=None,
        )

    return None
