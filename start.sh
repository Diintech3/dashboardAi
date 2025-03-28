#!/bin/bash

# Migrate database changes
python manage.py migrate

# Start Gunicorn server
gunicorn my_project.wsgi:application --bind 0.0.0.0:8000 --workers 4