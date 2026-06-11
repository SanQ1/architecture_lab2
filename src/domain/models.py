from .errors import DomainError
from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    id: int = None
    name: str = None
    price: float = None


@dataclass
class Order:
    user_id: str
    items: List[str]
    id: int = None


@dataclass
class User:
    id: str
    username: str
    password_hash: str

    def __post_init__(self):
        if not self.username:
            raise DomainError("Username cannot be empty")
