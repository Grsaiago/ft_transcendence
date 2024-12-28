#!/bin/bash

# Run makemigrations to ensure database migrations are up-to-date
echo "Running makemigrations..."
./manage.py makemigrations

# Run compilemessages to compile translation files (optional)
echo "Compiling messages..."
./manage.py compilemessages

# Run collectstatic to gather all static files for production
echo "Collecting static files..."
./manage.py collectstatic --noinput

# Exec into Daphne to run the server, this replaces the shell with the Daphne process
echo "Starting Daphne server..."
exec daphne -b 0.0.0.0 -p 8000 ft_transcendence.asgi:application

