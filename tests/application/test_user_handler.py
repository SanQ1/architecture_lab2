import pytest
from unittest.mock import MagicMock
from src.application.handlers import UserHandler

@pytest.fixture
def user_handler(mock_uow):
    user_factory = MagicMock()
    return UserHandler(uow=mock_uow, factory=user_factory)

def test_register_user_success(user_handler, mock_uow):
    user_handler.register_user(username="newuser", password="password123")
    
    mock_uow.users.add.assert_called_once()
    mock_uow.commit.assert_called_once()

def test_get_by_id(user_handler, mock_uow):
    mock_user = MagicMock()
    mock_uow.users.get_by_id.return_value = mock_user
    
    user = user_handler.get_by_id("1")
    
    assert user == mock_user
    mock_uow.users.get_by_id.assert_called_once_with("1")
