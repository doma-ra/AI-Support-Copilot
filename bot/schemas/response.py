from pydantic import BaseModel
from typing import List, Optional

class BotResponse(BaseModel):
    intent: str
    severity: str
    answer: str
    actions: List[str] = []
    kb_refs: List[str] = []
    escalate: bool = False
    handoff_note: Optional[str] = None
