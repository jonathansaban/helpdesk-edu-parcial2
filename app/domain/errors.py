class DomainError(Exception):
    """Error base del dominio."""


class ValidationError(DomainError):
    """Dato de entrada invalido."""
