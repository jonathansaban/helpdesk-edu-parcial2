import pytest

from app.domain.errors import DuplicateAssignmentError, UserNotFoundError
from app.models.enums import Role
from app.services.notifications import Notifier, WebhookNotifier
from app.services.tickets import TicketService
from app.services.users import UserService


@pytest.fixture
def users() -> UserService:
    return UserService()


@pytest.fixture
def webhook() -> WebhookNotifier:
    return WebhookNotifier()


@pytest.fixture
def service(users: UserService, webhook: WebhookNotifier) -> TicketService:
    return TicketService(users=users, notifier=webhook)


def new_ticket(service: TicketService, requester_id: int):
    return service.create(
        title="Falla",
        description="No enciende",
        category="hardware",
        priority="alta",
        requester_id=requester_id,
    )


def test_reasignar_al_mismo_tecnico_falla_sin_efectos(service, users, webhook):
    requester = users.register("Ana", Role.REQUESTER)
    tech = users.register("Luis", Role.TECHNICIAN)
    ticket = new_ticket(service, requester.id)
    service.assign(ticket.id, tech.id)

    historial_antes = len(ticket.history)
    notificaciones_antes = len(webhook.sent_payloads)

    with pytest.raises(DuplicateAssignmentError):
        service.assign(ticket.id, tech.id)

    assert len(ticket.history) == historial_antes
    assert len(webhook.sent_payloads) == notificaciones_antes


def test_asignacion_valida_notifica_por_webhook(service, users, webhook):
    requester = users.register("Ana", Role.REQUESTER)
    tech = users.register("Luis", Role.TECHNICIAN)
    ticket = new_ticket(service, requester.id)

    service.assign(ticket.id, tech.id)

    assert webhook.sent_payloads == [
        {"event": "assigned", "ticket_id": ticket.id, "user_id": tech.id}
    ]


def test_asignar_a_otro_tecnico_si_esta_permitido(service, users, webhook):
    requester = users.register("Ana", Role.REQUESTER)
    tech1 = users.register("Luis", Role.TECHNICIAN)
    tech2 = users.register("Marta", Role.TECHNICIAN)
    ticket = new_ticket(service, requester.id)
    service.assign(ticket.id, tech1.id)

    service.assign(ticket.id, tech2.id)

    assert ticket.assignee_id == tech2.id
    assert len(webhook.sent_payloads) == 2


def test_asignar_tecnico_inexistente_mantiene_validacion(service, users):
    requester = users.register("Ana", Role.REQUESTER)
    ticket = new_ticket(service, requester.id)

    with pytest.raises(UserNotFoundError):
        service.assign(ticket.id, 9999)


def test_webhook_notifier_cumple_el_contrato():
    assert isinstance(WebhookNotifier(), Notifier)


def test_notifier_abstracto_no_se_instancia():
    with pytest.raises(TypeError):
        Notifier()
