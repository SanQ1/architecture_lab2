import pytest
from app import app, db, User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    """Створюємо схему БД один раз для всіх тестів."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

@pytest.fixture(autouse=True)
def clean_data():
    """Очищуємо дані в таблицях перед кожним тестом, але не видаляємо самі таблиці."""
    yield
    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture
def auth_client():
    client = app.test_client()
    
    with app.app_context():
        if not User.query.filter_by(username="testuser").first():
            user = User(username="testuser", password=generate_password_hash("password123"), role="client")
            db.session.add(user)
            db.session.commit()

    response = client.post('/login', json={"username": "testuser", "password": "password123"})
    token = response.json['access_token']
    
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    
    return client

@pytest.fixture(autouse=True)
def cleanup_session():
    yield
    db.session.remove()
