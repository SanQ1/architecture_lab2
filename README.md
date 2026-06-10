# Лабораторна робота №2
Простий застосунок онлайн магазину. Працює локально на порту 5000.

## Перед запуском та тестуванням
Запустіть скрипт: ./setup.sh

## Запуск
Запустіть скрипт: ./start.sh

## Ручне тестування
Реєстрація:
```bash
curl -X POST http://localhost:5000/api/v1/register \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "password123"}'
```

Вхід та зберігання токена в змінну середовища:
```bash
TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/login \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "password123"}' | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
```

Перегляд товарів:
```bash
curl -X GET http://localhost:5000/api/v1/products
```

Додавання товару, використовуючи збережений токен:
```bash
curl -X POST http://localhost:5000/api/v1/products \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "Gaming Laptop", "price": 25000}'
```

Видалення товару:
```bash
curl -X DELETE http://localhost:5000/api/v1/products/1 \
     -H "Authorization: Bearer $TOKEN"
```

Створення замовлення:
```bash
curl -X POST http://localhost:5000/api/v1/orders \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"items": ["Mouse", "Keyboard"]}'
```

Видалення власного замовлення:
```bash
curl -X DELETE http://localhost:5000/api/v1/orders/1 \
     -H "Authorization: Bearer $TOKEN"
```

Додавання товару без токена(приведе до помилки):
```bash
curl -X POST http://localhost:5000/api/v1/products \
     -H "Content-Type: application/json" \
     -d '{"name": "Mouse", "price": 3000}'
```

## Unit-тести та інтеграційні тести
Для запуску unit-тестів та інтеграційних тестів використовуйте скрипт: ./test.sh
