#!/bin/bash

set -e

if ! command -v docker &> /dev/null; then
    echo "Docker не встановлено. Будь ласка, встановіть Docker для роботи з БД."
    exit 1
fi

echo "Оновлення системи та встановлення Python venv..."
sudo apt update && sudo apt upgrade -y
sudo apt install python3.13-venv -y

echo "Створення віртуального середовища..."
python3 -m venv venv
source venv/bin/activate

echo "Встановлення бібліотек..."
pip install flask flask-sqlalchemy flask-jwt-extended psycopg2-binary pytest

CONTAINER_NAME="lab2-db"

if [ "$(docker ps -aq -f name=^$CONTAINER_NAME$)" ]; then
    echo "Контейнер $CONTAINER_NAME вже існує. Запускаю його..."
    docker start $CONTAINER_NAME
else
    echo "Створюю та запускаю новий контейнер $CONTAINER_NAME..."
    docker run --name $CONTAINER_NAME \
        -e POSTGRES_USER=user \
        -e POSTGRES_PASSWORD=password \
        -e POSTGRES_DB=db \
        -p 5432:5432 \
        -d postgres:latest
fi

if [ ! -d "src" ]; then
    echo "Помилка: Папку 'src' не знайдено."
    exit 1
fi
