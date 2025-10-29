import json, time
from typing import Dict
from bot.schemas.response import BotResponse
from bot.providers.mock_provider import MockProvider

def handle_query(query: str, profile: str = "gastro") -> Dict:
    """Ruft den Provider auf, validiert Output, schreibt Log."""
    t0 = time.time()
    raw = MockProvider().generate(query, profile)
    resp = BotResponse(**raw).model_dump()
    _log_event(query, profile, resp, time.time() - t0)
    return resp

def _log_event(query: str, profile: str, resp: Dict, dt: float) -> None:
    rec = {
        "query": query,
        "profile": profile,
        "response": resp,
        "duration_ms": int(dt * 1000)
    }
    with open("logs/requests.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
