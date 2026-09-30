class DomainError(Exception):
    """Error base del dominio."""


class ValidationError(DomainError):
    """Dato de entrada invalido."""


class NotFoundError(DomainError):
    """No existe el recurso pedido."""


class TicketNotFoundError(NotFoundError):
    """No existe el ticket."""


class UserNotFoundError(NotFoundError):
    """No existe el usuario."""
