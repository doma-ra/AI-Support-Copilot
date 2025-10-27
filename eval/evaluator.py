import json, os
from pathlib import Path
from bot.router import route_faq
from bot.inference import validate_raw

DATA = Path("data/chats.jsonl")
OUT = Path("reports/metrics.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

def iter_queries():
    with open(DATA, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                obj = json.loads(line)
                yield obj["text"]

def main():
    total = 0
    valid_json = 0
    kb_hits = 0
    faq_hits = 0
    fallbacks = 0

    for q in iter_queries():
        total += 1
        res = route_faq(q)
        if res is None:
            # Fallback: hier wäre später der Modellaufruf; jetzt eskalieren wir sauber
            raw = '{"intent":"other","severity":"medium","answer":"Kein FAQ/KB-Treffer","actions":[],"kb_refs":[],"escalate":true,"handoff_note":"Bitte prüfen.","faq_id":null}'
            ok, parsed = validate_raw(raw)
            if ok:
                valid_json += 1
                fallbacks += 1
            else:
                # ungültiges JSON zählt nicht
                pass
            continue

        # Router gab BotResponse-Objekt zurück -> per Definition JSON-valid
        valid_json += 1
        if res.faq_id:
            faq_hits += 1
        if res.kb_refs:
            kb_hits += 1

    metrics = {
        "total": total,
        "json_valid_rate": (valid_json / total) if total else 0.0,
        "faq_hit_rate": (faq_hits / total) if total else 0.0,
        "kb_hit_rate": (kb_hits / total) if total else 0.0,
        "fallback_rate": (fallbacks / total) if total else 0.0,
        "notes": "Tokenkosten folgen, wenn der Modellpfad aktiv ist."
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
