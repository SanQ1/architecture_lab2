from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.repositories import (
    PostgresProductRepository, 
    PostgresOrderRepository, 
    PostgresUserRepository
)
from src.domain.factories.order_factory import OrderFactory
from src.domain.factories.user_factory import UserFactory
from src.application.handlers import ProductHandler, OrderHandler, UserHandler
from src.infrastructure.models import db

def get_uow() -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork()

def get_product_handler() -> ProductHandler:
    uow = get_uow()
    return ProductHandler(uow=uow)

def get_order_handler() -> OrderHandler:
    uow = get_uow()

    order_repo = PostgresOrderRepository(db.session)
    user_repo = PostgresUserRepository(db.session)

    factory = OrderFactory(order_repo=order_repo, user_repo=user_repo)
    return OrderHandler(uow=uow, factory=factory)

def get_user_handler() -> UserHandler:
    uow = get_uow()
    user_repo = PostgresUserRepository(db.session)
    factory = UserFactory(user_repo=user_repo)
    return UserHandler(uow=uow, factory=factory)
