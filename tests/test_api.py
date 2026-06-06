import pytest
import json
from app import db, User, Product

class TestIntegrationAPI:

    def test_register_user(self, client):
        """Перевірка реєстрації нового користувача (201)"""
        response = client.post('/register', 
            json={"username": "newuser", "password": "password123"})
        
        assert response.status_code == 201
        assert response.json['message'] == "Користувач створений"

    def test_add_product_success(self, auth_client):
        """Перевірка успішного додавання товару адміністратором (201)"""
        response = auth_client.post('/products', 
            json={"name": "Gaming Laptop", "price": 25000.0})
        
        assert response.status_code == 201
        assert response.json['message'] == "Товар додано"

    def test_add_product_unauthorized(self, client):
        """Перевірка, що неавторизований запит повертає 401"""
        response = client.post('/products', 
            json={"name": "Laptop", "price": 1000})
        
        assert response.status_code == 401

    def test_delete_nonexistent_product(self, auth_client):
        """Перевірка видалення неіснуючого товару (404)"""
        response = auth_client.delete('/products/999')
        
        assert response.status_code == 404
        assert response.json['message'] == "Товар не знайдено"

    def test_create_order_success(self, auth_client):
        response = auth_client.post('/orders',
            json={"items": ["product1", "product2"]})

        assert response.status_code == 201

    def test_invalid_product_data(self, auth_client):
        """Перевірка інваріантів: невалідні дані товару повертають 400"""
        response = auth_client.post('/products', 
            json={"name": "Ab", "price": 100.0})
        
        assert response.status_code == 400
