#!/bin/bash

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn deepwater.wsgi:application --bind 0.0.0.0:8000
