import pytest
from unittest.mock import Mock
from src.application.handlers import OrderHandler

def test_create_order_commits_transaction(mock_uow):
    factory = Mock()
    handler = OrderHandler(uow=mock_uow, factory=factory)
    
    mock_order = Mock()
    factory.create.return_value = mock_order
    
    handler.create_order(user_id="u1", items=["A"])
    
    mock_uow.orders.add.assert_called_once_with(mock_order)
    mock_uow.commit.assert_called_once()

def test_create_order_failure_rollback(mock_uow):
    factory = Mock()
    handler = OrderHandler(uow=mock_uow, factory=factory)

    mock_uow.orders.add.side_effect = Exception("DB error")

    with pytest.raises(Exception, match="DB error"):
        handler.create_order(user_id="u1", items=["Item1"])

    mock_uow.commit.assert_not_called()
