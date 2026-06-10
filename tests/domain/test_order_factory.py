import pytest
from src.domain.factories.order_factory import OrderFactory
from src.domain.errors import DomainError
from unittest.mock import Mock

def test_create_order_successfully():
    user_repo = Mock()
    user_repo.get_by_id.return_value = True 
    order_repo = Mock()
    
    factory = OrderFactory(order_repo=order_repo, user_repo=user_repo)
    
    items = ["Mouse", "Keyboard"]
    order = factory.create(user_id="user123", items=items)
    
    assert order.user_id == "user123"
    assert order.items == ["Mouse", "Keyboard"]
    assert order.id is None 

def test_create_order_fails_if_user_not_exists():
    user_repo = Mock()
    user_repo.get_by_id.return_value = None 
    factory = OrderFactory(order_repo=Mock(), user_repo=user_repo)
    
    with pytest.raises(DomainError, match="Користувача з ID user123 не існує"):
        factory.create(user_id="user123", items=["Item"])

def test_create_order_fails_if_items_empty():
    user_repo = Mock()
    user_repo.get_by_id.return_value = True
    factory = OrderFactory(order_repo=Mock(), user_repo=user_repo)
    
    with pytest.raises(DomainError, match="Замовлення не може бути порожнім"):
        factory.create(user_id="user123", items=[])
