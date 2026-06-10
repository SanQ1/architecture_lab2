from src.application.unit_of_work import AbstractUnitOfWork
from src.infrastructure.models import db
from src.infrastructure.repositories import PostgresProductRepository, PostgresOrderRepository, PostgresUserRepository

class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.products = PostgresProductRepository(db.session)
        self.orders = PostgresOrderRepository(db.session)
        self.users = PostgresUserRepository(db.session)
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()
