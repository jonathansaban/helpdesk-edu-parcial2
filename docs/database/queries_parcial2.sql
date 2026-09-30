-- a) Tickets abiertos con el nombre del solicitante (JOIN)
SELECT t.id, t.title, t.status, u.name AS solicitante
FROM tickets t
JOIN users u ON u.id = t.requester_id
WHERE t.status = 'open'
ORDER BY t.id;

-- b) Conteo de tickets por tecnico asignado, sin conteos cero, de mayor a menor
SELECT u.id, u.name, COUNT(t.id) AS total_tickets
FROM users u
LEFT JOIN tickets t ON t.assignee_id = u.id
WHERE u.role = 'technician'
GROUP BY u.id, u.name
HAVING COUNT(t.id) > 0
ORDER BY total_tickets DESC, u.id;

-- c) Tickets sin comentarios (NOT EXISTS)
SELECT t.id, t.title
FROM tickets t
WHERE NOT EXISTS (
    SELECT 1 FROM comments c WHERE c.ticket_id = t.id
)
ORDER BY t.id;

-- d) ON DELETE CASCADE sobre el historial, dentro de una transaccion con ROLLBACK
BEGIN;
SELECT COUNT(*) AS historial_inicial FROM ticket_history WHERE ticket_id = 1;
DELETE FROM tickets WHERE id = 1;
SELECT COUNT(*) AS historial_tras_delete FROM ticket_history WHERE ticket_id = 1;
ROLLBACK;
SELECT COUNT(*) AS historial_tras_rollback FROM ticket_history WHERE ticket_id = 1;
