DROP TABLE IF EXISTS ticket_history, comments, tickets, users CASCADE;

CREATE TABLE users (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('requester', 'technician'))
);

CREATE TABLE tickets (
    id           SERIAL PRIMARY KEY,
    title        VARCHAR(120) NOT NULL,
    description  TEXT NOT NULL,
    category     VARCHAR(40) NOT NULL,
    priority     VARCHAR(20) NOT NULL,
    status       VARCHAR(20) NOT NULL DEFAULT 'open'
                 CHECK (status IN ('open', 'in_progress', 'closed')),
    requester_id INTEGER NOT NULL REFERENCES users(id),
    assignee_id  INTEGER REFERENCES users(id)
);

CREATE TABLE comments (
    id         SERIAL PRIMARY KEY,
    ticket_id  INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    author_id  INTEGER NOT NULL REFERENCES users(id),
    body       TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ticket_history (
    id         SERIAL PRIMARY KEY,
    ticket_id  INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    action     VARCHAR(40) NOT NULL,
    detail     TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO users (name, role) VALUES
    ('Ana',   'requester'),
    ('Bruno', 'requester'),
    ('Luis',  'technician'),
    ('Marta', 'technician'),
    ('Sofia', 'technician');

INSERT INTO tickets (title, description, category, priority, status, requester_id, assignee_id) VALUES
    ('No imprime',        'La impresora no responde', 'Hardware', 'High',   'open',        1, 3),
    ('No ingresa al SIS', 'Error de credenciales',    'Software', 'Medium', 'open',        2, NULL),
    ('Correo lento',      'Tarda en abrir',           'Redes',    'Low',    'in_progress', 1, 3),
    ('Monitor parpadea',  'Falla intermitente',       'Hardware', 'Medium', 'open',        2, 4),
    ('Acceso VPN',        'Solicitud de acceso',      'Redes',    'Low',    'closed',      1, 4);

INSERT INTO comments (ticket_id, author_id, body) VALUES
    (1, 3, 'Revisando el cable de la impresora'),
    (1, 1, 'Gracias, sigo pendiente'),
    (3, 3, 'Se reinicio el servidor de correo');

INSERT INTO ticket_history (ticket_id, action, detail) VALUES
    (1, 'created',  'Ticket creado por Ana'),
    (1, 'assigned', 'Asignado a Luis'),
    (3, 'created',  'Ticket creado por Ana'),
    (3, 'assigned', 'Asignado a Luis'),
    (4, 'created',  'Ticket creado por Bruno');
