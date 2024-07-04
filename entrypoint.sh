#!/bin/bash

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec daphne -b 0.0.0.0 -p 8000 deepwater.asgi:application
