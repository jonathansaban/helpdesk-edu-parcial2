import pytest

from app.domain.errors import TicketNotFoundError
from app.models.enums import Role
from app.services.tickets import TicketService
from app.services.users import UserService


@pytest.fixture
def users() -> UserService:
    return UserService()


@pytest.fixture
def service(users: UserService) -> TicketService:
    return TicketService(users=users)


def new_ticket(service: TicketService, requester_id: int):
    return service.create(
        title="Falla",
        description="No enciende",
        category="hardware",
        priority="alta",
        requester_id=requester_id,
    )


def test_watchers_sin_tecnico(service, users):
    requester = users.register("Ana", Role.REQUESTER)
    ticket = new_ticket(service, requester.id)

    result = service.watchers(ticket.id)

    assert [u.id for u in result] == [requester.id]


def test_watchers_con_tecnico_distinto(service, users):
    requester = users.register("Ana", Role.REQUESTER)
    technician = users.register("Luis", Role.TECHNICIAN)
    ticket = new_ticket(service, requester.id)
    service.assign_technician(ticket.id, technician.id)

    result = service.watchers(ticket.id)

    assert [u.id for u in result] == [requester.id, technician.id]


def test_watchers_ticket_inexistente(service):
    with pytest.raises(TicketNotFoundError):
        service.watchers(9999)


def test_watchers_deduplica_mismo_usuario(service, users):
    requester = users.register("Ana", Role.REQUESTER)
    ticket = new_ticket(service, requester.id)
    ticket.assignee_id = requester.id  # datos controlados: mismo id en ambos roles

    result = service.watchers(ticket.id)

    assert [u.id for u in result] == [requester.id]
