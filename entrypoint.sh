#!/bin/ash

echo "Apply database migrations"
python manage.py migrate
echo 'Migration made, running server'
python manage.py runserver 0.0.0.0:8000
exec "$@"
