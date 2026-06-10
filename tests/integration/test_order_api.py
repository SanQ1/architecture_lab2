import pytest
from src.infrastructure.models import UserEntity

def test_create_order_success(client, auth_headers, db_session):
    user = UserEntity(id="test-user-id", username="testuser", password_hash="hash")
    db_session.add(user)
    db_session.commit()

    payload = {"items": ["Mouse"]}
    response = client.post('/api/v1/orders', json=payload, headers=auth_headers)
    
    assert response.status_code == 201

def test_create_order_unauthorized(client):
    """Перевірка доступу без токена (401 Unauthorized)"""
    response = client.post('/api/v1/orders', json={"items": ["Mouse"]})
    assert response.status_code == 401

def test_create_order_bad_request(client, auth_headers, db_session):
    """Перевірка валідації (порожні товари)"""
    user = UserEntity(id="test-user-id", username="testuser", password_hash="hash")
    db_session.add(user)
    db_session.commit()

    response = client.post('/api/v1/orders', json={"items": []}, headers=auth_headers)
    assert response.status_code == 400
