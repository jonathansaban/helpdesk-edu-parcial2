import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.entities import Ticket
from app.models.enums import TicketStatus
from app.repositories.base import TicketRepository
from app.repositories.sqlalchemy import Base, SqlAlchemyTicketRepository

OPEN = TicketStatus.OPEN.value
IN_PROGRESS = TicketStatus.IN_PROGRESS.value


def make_engine():
    """Engine SQLite en memoria; StaticPool hace que todas las sesiones compartan la conexion."""
    engine = create_engine(
        "sqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    return engine


def make_ticket(ticket_id: int, status: str) -> Ticket:
    return Ticket(
        id=ticket_id,
        title=f"Ticket {ticket_id}",
        description="Caso de prueba",
        category="hardware",
        priority="alta",
        requester_id=1,
        status=status,
    )


def test_count_by_status_desde_sesion_nueva_tras_commit():
    engine = make_engine()
    Session = sessionmaker(bind=engine)

    # Sesion 1: crear 3 tickets (2 open + 1 in_progress), confirmar y cerrar
    session1 = Session()
    repo1 = SqlAlchemyTicketRepository(session1)
    repo1.add(make_ticket(1, OPEN))
    repo1.add(make_ticket(2, OPEN))
    repo1.add(make_ticket(3, IN_PROGRESS))
    session1.commit()
    session1.close()

    # Sesion 2 NUEVA sobre el mismo engine: si el dato aparece, persistio
    session2 = Session()
    result = SqlAlchemyTicketRepository(session2).count_by_status()
    session2.close()

    assert result == {OPEN: 2, IN_PROGRESS: 1}
    assert sum(result.values()) == 3


def test_count_by_status_base_vacia():
    engine = make_engine()  # engine independiente, sin datos
    session = sessionmaker(bind=engine)()

    assert SqlAlchemyTicketRepository(session).count_by_status() == {}
    session.close()


def test_interfaz_abstracta_no_cambia():
    assert not hasattr(TicketRepository, "count_by_status")
    with pytest.raises(TypeError):
        TicketRepository()
