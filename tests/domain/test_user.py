import pytest
from src.domain.models import User
from src.domain.errors import DomainError

def test_user_creation():
    user = User(id="1", username="testuser", password_hash="hashed_pass")
    assert user.username == "testuser"
    assert user.password_hash == "hashed_pass"

def test_user_invalid_username():
    with pytest.raises(DomainError):
        User(id="1", username="", password_hash="pass")
