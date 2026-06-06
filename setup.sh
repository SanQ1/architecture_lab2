#!/bin/bash

set -e

# перевірка наявності Docker
if ! command -v docker &> /dev/null; then
    echo "Docker не встановлено. Будь ласка, встановіть Docker для роботи з БД."
    exit 1
fi

sudo apt update && sudo apt upgrade -y
sudo apt install python3.13-venv -y

echo "Створення віртуального середовища..."
python3 -m venv venv
source venv/bin/activate

echo "Встановлення залежностей..."
pip install flask flask-sqlalchemy flask-jwt-extended psycopg2-binary pytest

# Перевірка, чи контейнер lab1-db вже існує
if [ "$(docker ps -aq -f name=^lab1-db$)" ]; then
    echo "Контейнер lab1-db вже існує. Запускаю його..."
    docker start lab1-db
else
    echo "Створюю та запускаю новий контейнер lab1-db..."
    docker run --name lab1-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=db -p 5432:5432 -d postgres:latest
fi
