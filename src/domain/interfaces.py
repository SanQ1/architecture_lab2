from abc import ABC, abstractmethod
from .models import (
    User,
    Product,
    Order
)


class AbstractProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int) -> Product:
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self, product_id: int) -> None:
        raise NotImplementedError


class AbstractUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: str) -> User | None:
        raise NotImplementedError


class AbstractOrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, order_id: str) -> Order | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, order_id: str) -> None:
        raise NotImplementedError
