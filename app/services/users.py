from app.domain.errors import UserNotFoundError
from app.models.entities import User
from app.models.enums import Role


class UserService:
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._next_id = 1

    def register(self, name: str, role: Role) -> User:
        user = User(id=self._next_id, name=name, role=role)
        self._users[user.id] = user
        self._next_id += 1
        return user

    def require(self, user_id: int) -> User:
        """Devuelve el usuario o lanza UserNotFoundError."""
        user = self._users.get(user_id)
        if user is None:
            raise UserNotFoundError(f"Usuario {user_id} no encontrado")
        return user
