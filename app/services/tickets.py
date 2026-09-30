from app.models.entities import Ticket
from app.models.enums import TicketStatus


class TicketService:
    def __init__(self) -> None:
        self._tickets: list[Ticket] = []
        self._next_id = 1

    def create(self, title, description, category, priority, requester_id) -> Ticket:
        ticket = Ticket(
            id=self._next_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            requester_id=requester_id,
        )
        self._tickets.append(ticket)
        self._next_id += 1
        return ticket

    def assign_technician(self, ticket_id: int, technician_id: int) -> None:
        for ticket in self._tickets:
            if ticket.id == ticket_id:
                ticket.assignee_id = technician_id
                return
        raise ValueError(f"Ticket {ticket_id} not found")

    # --- Semana 9 ---
    def list_by_technician(self, technician_id: int) -> list[Ticket]:
        """Return tickets assigned to one technician."""
        return [t for t in self._tickets if t.assignee_id == technician_id]

    def list_by_category(self, category: str) -> list[Ticket]:
        """Return tickets that belong to one category."""
        return [t for t in self._tickets if t.category == category]

    def list_by_status(self, status: str | TicketStatus) -> list[Ticket]:
        """Return tickets with a specific status."""
        status_value = status.value if isinstance(status, TicketStatus) else status
        return [t for t in self._tickets if t.status == status_value]