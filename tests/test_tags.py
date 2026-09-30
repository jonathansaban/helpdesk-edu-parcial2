import pytest

from app.domain.errors import ValidationError
from app.models.entities import Ticket


def make_ticket(ticket_id: int = 1) -> Ticket:
    return Ticket(
        id=ticket_id,
        title="Falla",
        description="No enciende",
        category="hardware",
        priority="alta",
        requester_id=1,
    )


def test_normaliza_y_evita_duplicados():
    t = make_ticket()
    t.add_tag("  Red  ")
    t.add_tag("RED")
    t.add_tag("wifi")
    assert t.tags == ("red", "wifi")


def test_rechaza_vacias_y_espacios():
    t = make_ticket()
    with pytest.raises(ValidationError):
        t.add_tag("")
    with pytest.raises(ValidationError):
        t.add_tag("    ")
    assert t.tags == ()


def test_tags_independientes_entre_tickets():
    a = make_ticket(1)
    b = make_ticket(2)
    a.add_tag("urgente")
    assert a.tags == ("urgente",)
    assert b.tags == ()


def test_tags_devuelve_tupla():
    t = make_ticket()
    t.add_tag("x")
    assert isinstance(t.tags, tuple)


def test_no_permite_reasignar_tags():
    t = make_ticket()
    with pytest.raises(AttributeError):
        t.tags = ["hack"]
