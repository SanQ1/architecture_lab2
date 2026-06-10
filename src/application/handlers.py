import uuid
from src.application.unit_of_work import AbstractUnitOfWork
from src.domain.factories.user_factory import UserFactory
from src.domain.factories.order_factory import OrderFactory
from src.domain.models import Product
from src.domain.errors import DomainError

class ProductHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def add_product(self, name: str, price: float) -> str:
        with self.uow:
            product = Product(name=name, price=price)
            self.uow.products.add(product)
            self.uow.commit()
            return product.id

    def delete_product(self, product_id: str) -> None:
        with self.uow:
            self.uow.products.delete(product_id)
            self.uow.commit()

    def list_all(self):
        with self.uow:
            return self.uow.products.list()

class OrderHandler:
    def __init__(self, uow: AbstractUnitOfWork, factory: OrderFactory):
        self.uow = uow
        self.factory = factory

    def create_order(self, user_id: str, items: list[str]) -> str:
        with self.uow:
            order = self.factory.create(user_id=user_id, items=items)
            self.uow.orders.add(order)
            self.uow.commit()
            return order.id

    def delete_order(self, order_id: str) -> None:
        with self.uow:
            self.uow.orders.delete(order_id)
            self.uow.commit()

class UserHandler:
    def __init__(self, uow: AbstractUnitOfWork, factory: UserFactory):
        self.uow = uow
        self.factory = factory

    def register_user(self, username: str, password: str) -> str:
        with self.uow:
            user = self.factory.create(username=username, password=password)
            self.uow.users.add(user)
            self.uow.commit()
            return user.id

    def get_by_id(self, user_id: str):
        with self.uow:
            return self.uow.users.get_by_id(user_id)
