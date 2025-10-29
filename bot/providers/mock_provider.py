from typing import Dict
from .base import AbstractProvider

class MockProvider(AbstractProvider):
    def generate(self, prompt: str, profile: str) -> Dict:
        # Minimaler, immer valider Fallback. Migration deiner Logik folgt später.
        base = {
            "intent": "other",
            "severity": "medium",
            "answer": "Kein KB-Treffer. Bitte präzisieren oder eskalieren.",
            "actions": [],
            "kb_refs": [],
            "escalate": True,
            "handoff_note": "Zeit, Gerät, Version, Logs anhängen."
        }
        # Sehr einfache Profil-Note, damit IT/Gastro unterscheidbar ist
        if profile == "it":
            base["handoff_note"] = "OS, Standort, Ticket-ID, Logs anhängen."
        return base
