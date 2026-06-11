import pytest
from src.main import db, app 
from unittest.mock import Mock, MagicMock
from src.application.handlers import ProductHandler, OrderHandler
from sqlalchemy import create_engine
from src.infrastructure.models import Base
from src.infrastructure.models import UserEntity, ProductEntity, OrderEntity
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool

@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)
    scoped = scoped_session(session_factory)

    db.session = scoped

    yield scoped()

    scoped.remove()
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def auth_headers():
    """Повертає словник із заголовком Authorization для запитів."""
    with app.app_context():
        token = create_access_token(identity="test-user-id")
        return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_uow():
    """Фікстура для створення моку Unit of Work."""
    uow = MagicMock()
    uow.__enter__.return_value = uow 
    return uow

@pytest.fixture
def product_handler(mock_uow):
    """Фікстура для ProductHandler з уже підготовленим моком UoW."""
    return ProductHandler(uow=mock_uow)

@pytest.fixture
def order_handler(mock_uow):
    """Фікстура для OrderHandler."""
    factory = Mock() 
    return OrderHandler(uow=mock_uow, factory=factory)

