import json, re
from typing import List, Dict, Optional

def load_index(path: str = "kb/index.json") -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

_IDX = None
def _ensure_idx():
    global _IDX
    if _IDX is None:
        _IDX = load_index()

def retrieve_best(query: str) -> Optional[Dict]:
    """
    Sehr einfacher Keyword-Retriever: Score = Anzahl Keyword-Treffer.
    Gibt das beste Item oder None zurück.
    """
    _ensure_idx()
    q = query.lower()
    best, best_score = None, 0
    for item in _IDX:
        score = sum(1 for kw in item["keywords"] if re.search(r"\b" + re.escape(kw) + r"\b", q))
        if score > best_score:
            best, best_score = item, score
    return best if best_score > 0 else None
