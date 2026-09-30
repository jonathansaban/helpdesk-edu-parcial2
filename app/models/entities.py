from dataclasses import dataclass, field
from typing import Optional

from app.domain.errors import ValidationError


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

    def add_tag(self, tag: str) -> None:
        """Agrega una etiqueta normalizada (strip + lower), sin vacias ni duplicados."""
        clean = tag.strip().lower()
        if not clean:
            raise ValidationError("La etiqueta no puede estar vacia")
        if clean not in self._tags:
            self._tags.append(clean)
