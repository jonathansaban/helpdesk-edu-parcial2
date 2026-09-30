from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Ticket:
    id: int
    title: str
    description: str
    category: str
    priority: str
    requester_id: int
    status: str = "open"
    assignee_id: Optional[int] = None