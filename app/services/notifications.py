from abc import ABC, abstractmethod


class Notifier(ABC):
    """Contrato de notificaciones: el servicio solo conoce esta interfaz."""

    @abstractmethod
    def notify(self, event: str, ticket_id: int, user_id: int) -> None:
        """Avisa a un usuario que ocurrio un evento en un ticket."""


class WebhookNotifier(Notifier):
    """Simula un canal webhook: guarda lo recibido, sin HTTP ni print."""

    def __init__(self) -> None:
        self.sent_payloads: list[dict] = []

    def notify(self, event: str, ticket_id: int, user_id: int) -> None:
        self.sent_payloads.append(
            {"event": event, "ticket_id": ticket_id, "user_id": user_id}
        )
