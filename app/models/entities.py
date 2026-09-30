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
    _tags: list[str] = field(default_factory=list, init=False, repr=False)

    @property
    def tags(self) -> tuple[str, ...]:
        """Solo lectura: devuelve una tupla, no la lista interna."""
        return tuple(self._tags)
