#!/bin/bash

echo "Ожидание PostgreSQL."
while ! nc -z $HOST $PORT; do
  sleep 1
done

echo "База доступна. Инициализация."
python init_db.py

echo "Запуск бота."
exec python script.py
