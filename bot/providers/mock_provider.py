from typing import Dict

from .base import AbstractProvider

GASTRO_RULES = [
    {
        "keywords": ("kartenzahlung", "zahlung", "terminal", "karte"),
        "intent": "payment",
        "answer": "Starte das Kartenterminal neu und prüfe Netzwerk/Internet. Wenn weiter Fehler, Logs anhängen und eskalieren.",
        "kb_refs": ["faq:PAY-001"],
    },
    {
        "keywords": ("drucker", "bon", "bondrucker"),
        "intent": "printer",
        "answer": "Prüfe Papier, Verbindung und wähle den Bondrucker in der Kasse neu aus. Testdruck auslösen.",
        "kb_refs": ["kb:PRN-quickcheck"],
    },
]

IT_RULES = [
    {
        "keywords": ("vpn",),
        "intent": "vpn",
        "answer": "VPN-Client neu verbinden. Prüfe Credentials und Gateway. Wenn weiter Fehler, Log-Export anhängen.",
        "kb_refs": ["kb_it:VPN-001"],
    },
    {
        "keywords": ("sso", "login"),
        "intent": "sso",
        "answer": "SSO-Session im Browser leeren und erneut anmelden. Prüfe Zeitdrift und IdP-Status.",
        "kb_refs": ["kb_it:SSO-101"],
    },
]

def _match(query: str, profile: str) -> Dict:
    text = query.lower()
    rules = GASTRO_RULES if profile == "gastro" else IT_RULES
    for rule in rules:
        if any(k in text for k in rule["keywords"]):
            return {
                "intent": rule["intent"],
                "severity": "medium",
                "answer": rule["answer"],
                "actions": [],
                "kb_refs": rule["kb_refs"],
                "escalate": False,
                "handoff_note": None,
            }
    # Default
    return {
        "intent": "other",
        "severity": "medium",
        "answer": "Kein KB-Treffer. Bitte präzisieren oder eskalieren.",
        "actions": [],
        "kb_refs": [],
        "escalate": True,
        "handoff_note": "Zeit, Gerät, Version, Logs anhängen." if profile == "gastro" else "OS, Standort, Ticket-ID, Logs anhängen.",
    }

class MockProvider(AbstractProvider):
    def generate(self, prompt: str, profile: str) -> Dict:
        return _match(prompt, profile)
