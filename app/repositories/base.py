from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.entities import Ticket


class TicketRepository(ABC):
    """Contrato de persistencia de tickets."""

    @abstractmethod
    def add(self, ticket: Ticket) -> Ticket:
        """Guarda un ticket nuevo."""

    @abstractmethod
    def by_id(self, ticket_id: int) -> Ticket | None:
        """Devuelve el ticket o None si no existe."""

    @abstractmethod
    def list(self, *, status=None, assignee_id=None, requester_id=None) -> list[Ticket]:
        """Lista tickets; los filtros se pasan por nombre."""

    @abstractmethod
    def next_id(self) -> int:
        """Siguiente id disponible."""

    @abstractmethod
    def update(self, ticket: Ticket) -> None:
        """Escribe los cambios de un ticket existente."""
