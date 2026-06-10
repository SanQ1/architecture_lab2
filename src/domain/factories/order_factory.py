from src.domain.models import Order
from src.domain.interfaces import AbstractOrderRepository, AbstractUserRepository
from src.domain.errors import DomainError

class OrderFactory:
    def __init__(self, order_repo: AbstractOrderRepository, user_repo: AbstractUserRepository):
        self._order_repo = order_repo
        self._user_repo = user_repo

    def create(self, user_id: str, items: list[str]) -> Order:
        if not self._user_repo.get_by_id(user_id):
            raise DomainError(f"Користувача з ID {user_id} не існує")

        if not items:
            raise DomainError("Замовлення не може бути порожнім")
        
        return Order(
            user_id=user_id, 
            items=items
        )
