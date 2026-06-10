from src.domain.models import User
from src.domain.interfaces import AbstractUserRepository
from src.domain.errors import DomainError
from werkzeug.security import generate_password_hash

class UserFactory:
    def __init__(self, user_repo: AbstractUserRepository):
        self._user_repo = user_repo

    def create(self, username: str, password: str) -> User:
        if self._user_repo.get_by_username(username):
            raise DomainError(f"Користувач з іменем {username} вже існує")
        
        if len(password) < 8:
            raise DomainError("Пароль занадто короткий")
            
        password_hash = generate_password_hash(password)
        
        return User(id=None, username=username, password_hash=password_hash)
