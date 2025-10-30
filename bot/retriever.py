import os, json, re
from typing import List, Dict, Optional

def load_index(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def index_path_for(profile: str) -> str:
    return "kb_it/index.json" if profile.lower() == "it" else "kb/index.json"

def retrieve_best(query: str, profile: Optional[str] = None) -> Optional[Dict]:
    """
    Einfacher Keyword-Retriever. Profil 'gastro' (Default) oder 'it'.
    Profil kommt aus Param oder env KB_PROFILE.
    """
    profile = (profile or os.getenv("KB_PROFILE", "gastro")).lower()
    idx = load_index(index_path_for(profile))
    q = query.lower()
    best, best_score = None, 0
    for item in idx:
        score = sum(1 for kw in item["keywords"] if re.search(r"\b" + re.escape(kw) + r"\b", q))
        if score > best_score:
            best, best_score = item, score
    return best if best_score > 0 else None

