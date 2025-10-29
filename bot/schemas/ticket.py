from pydantic import BaseModel, Field
from typing import Optional, Literal

Priority = Literal["low", "medium", "high"]

class Ticket(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)
    profile: Literal["gastro", "it"] = "gastro"
    priority: Priority = "medium"
    customer: Optional[str] = None
    correlation_id: Optional[str] = None
