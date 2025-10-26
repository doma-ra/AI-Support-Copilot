from pydantic import BaseModel
from typing import List, Optional, Literal

Intent = Literal["pos","payment","reservation","receipt","it_login","it_vpn","printer","other"]
Severity = Literal["low","medium","high"]

class BotResponse(BaseModel):
    intent: Intent
    severity: Severity
    answer: str
    actions: List[str] = []
    kb_refs: List[str] = []
    escalate: bool = False
    handoff_note: Optional[str] = None
    faq_id: Optional[str] = None
