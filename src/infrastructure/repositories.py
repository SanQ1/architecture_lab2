from src.domain.interfaces import (
    AbstractProductRepository,
    AbstractOrderRepository,
    AbstractUserRepository
)
from src.domain.models import (
    Product,
    Order,
    User
)
from .models import (
    db,
    ProductEntity,
    OrderEntity,
    UserEntity
)
from .mappers import (
    ProductMapper,
    OrderMapper,
    UserMapper
)

class PostgresProductRepository(AbstractProductRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product: Product) -> None:
        entity = ProductMapper.to_entity(product)
        self.session.add(entity)
        self.session.commit()

    def get_by_id(self, product_id: str) -> Product | None:
        entity = self.session.get(ProductEntity, product_id)
        return ProductMapper.to_domain(entity) if entity else None

    def list(self):
        return self.session.query(ProductEntity).all()

    def delete(self, product_id: int) -> None:
        product = self.session.query(ProductEntity).filter_by(id=product_id).first()
        if product:
            self.session.delete(product)


class PostgresOrderRepository(AbstractOrderRepository):
    def __init__(self, session):
        self.session = session

    def add(self, order: Order) -> int:
        entity = OrderMapper.to_entity(order)
        db.session.add(entity)
        db.session.flush()
        db.session.refresh(entity)

        order.id = entity.id
        return order.id

    def get_by_id(self, order_id: str) -> Order | None:
        entity = db.session.get(OrderEntity, order_id)
        return OrderMapper.to_domain(entity) if entity else None

    def delete(self, order_id):
        order = self.session.query(OrderEntity).filter_by(id=order_id).first()
        if order:
            self.session.delete(order)


class PostgresUserRepository(AbstractUserRepository):
    def __init__(self, session):
        self.session = session

    def add(self, user: User) -> None:
        entity = UserMapper.to_entity(user)
        self.session.add(entity)

    def get_by_username(self, username: str) -> User | None:
        entity = self.session.query(UserEntity).filter_by(username=username).first()
        if not entity:
            return None
        return UserMapper.to_domain(entity)

    def get_by_id(self, user_id: str) -> User | None:
        entity = self.session.get(UserEntity, user_id)
        return UserMapper.to_domain(entity) if entity else None
