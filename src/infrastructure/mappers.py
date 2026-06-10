from src.domain.models import (
    Product,
    Order,
    User
)
from src.infrastructure.models import (
    ProductEntity,
    OrderEntity,
    UserEntity
)

class ProductMapper:
    @staticmethod
    def to_domain(entity: ProductEntity) -> Product:
        return Product(
            id=entity.id,
            name=entity.name,
            price=entity.price
        )

    @staticmethod
    def to_entity(domain: Product) -> ProductEntity:
        entity = ProductEntity(
            name=domain.name,
            price=domain.price
        )
        if domain.id is not None:
            entity.id = domain.id
        return entity


class OrderMapper:
    @staticmethod
    def to_domain(entity: OrderEntity) -> Order:
        return Order(
            id=entity.id,
            user_id=entity.user_id,
            items=entity.items.split(", ") if entity.items else []
        )

    @staticmethod
    def to_entity(domain: Order) -> OrderEntity:
        entity = OrderEntity(
            user_id=domain.user_id,
            items=", ".join(domain.items)
        )
        if domain.id is not None:
            entity.id = domain.id
        return entity


class UserMapper:
    @staticmethod
    def to_domain(entity: UserEntity) -> User:
        return User(id=entity.id, username=entity.username, password_hash=entity.password_hash)

    @staticmethod
    def to_entity(domain: User) -> UserEntity:
        return UserEntity(id=domain.id, username=domain.username, password_hash=domain.password_hash)
