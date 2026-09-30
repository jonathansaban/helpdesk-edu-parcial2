# Parcial 2: Programación II (HelpDesk EDU)

Semanas 7 a 11 | Python, PostgreSQL, SQLAlchemy y proyecto HelpDesk EDU

## Cómo reproducirlo

### Pruebas de Python

    uv sync
    uv run pytest -q

### Consultas SQL (PostgreSQL en Docker)

    docker run --name helpdesk-pg -e POSTGRES_USER=helpdesk -e POSTGRES_PASSWORD=helpdesk123 -e POSTGRES_DB=helpdesk -p 5433:5432 -d postgres:17.11-alpine
    Get-Content docs\database\database.sql | docker exec -i helpdesk-pg psql -U helpdesk -d helpdesk
    Get-Content docs\database\queries_parcial2.sql | docker exec -i helpdesk-pg psql -U helpdesk -d helpdesk -e

Nota: se usó la imagen `postgres:17.11-alpine` porque ya estaba descargada localmente. El puerto 5433 del host se mapea al 5432 del contenedor.

## Resultados de las pruebas

- Antes de los cambios: `3 passed`, sin fallos previos.
- Después de los cambios: `21 passed`, sin fallos.

## Archivos por ejercicio

| Ejercicio | Rama | Archivos |
|---|---|---|
| 1. Etiquetas y encapsulamiento | feature_etiquetasEncapsuladas | app/models/entities.py, app/domain/errors.py, tests/test_tags.py |
| 2. Observadores | feature_watchers | app/services/tickets.py, app/services/users.py, app/models/entities.py, app/models/enums.py, app/domain/errors.py, tests/test_watchers.py |
| 3. Excepciones y polimorfismo | feature_asignacionDuplicadaWebhook | app/domain/errors.py, app/services/tickets.py, app/services/notifications.py, app/models/entities.py, tests/test_assign_duplicate.py |
| 4. SQL e integridad referencial | feature_consultasSql | docs/database/database.sql, docs/database/queries_parcial2.sql, docs/database/salida_parcial2.txt |
| 5. Consulta agregada con SQLAlchemy | feature_countByStatus | app/repositories/base.py, app/repositories/sqlalchemy.py, tests/test_count_by_status.py, pyproject.toml, uv.lock |

Cada ejercicio se desarrolló en su propia rama `feature_...`, con commits por cada avance, y se integró a `main` con un merge `--no-ff`.

## Evidencia SQL

La salida completa de las cuatro consultas está en `docs/database/salida_parcial2.txt`. En la demostración de cascada (consulta d), el historial del ticket 1 pasa de 2 a 0 tras el `DELETE` y vuelve a 2 tras el `ROLLBACK`. Al finalizar, los conteos de las tablas son los mismos que al inicio (5 usuarios, 5 tickets, 3 comentarios, 5 eventos de historial).

## Limitaciones

- Las etiquetas (`_tags`) viven solo en memoria; no se persisten en SQL ni requieren migración.
- El proyecto base era de la semana 9, así que `User`, `UserService`, `Notifier`, el historial y el repositorio se crearon con lo mínimo necesario para cada ejercicio.
- `WebhookNotifier` es una simulación: guarda los payloads en `sent_payloads`, sin HTTP.
- `count_by_status()` existe solo en `SqlAlchemyTicketRepository`; la interfaz abstracta `TicketRepository` no se modificó.
- El modelo ORM cubre solo la tabla de tickets; comentarios e historial no están mapeados en SQLAlchemy.
- Las pruebas de SQLAlchemy usan SQLite en memoria con `StaticPool`, no PostgreSQL.
