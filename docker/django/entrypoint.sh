#!/bin/bash

echo "Running makemigrations..."
./manage.py makemigrations
./manage.py migrate

echo "Compiling messages..."
./manage.py compilemessages

echo "Collecting static files..."
./manage.py collectstatic --noinput

# Exec into Daphne to run the server, this replaces the shell with the Daphne process
# ensuring that signals received by the container are captured by the daphne server
echo "Starting Daphne server..."
# exec daphne -b 0.0.0.0 -p 443 -e ssl:443:privateKey=/cert/key.pem:certKey=/cert/cert.pem ft_transcendence.asgi:application
exec daphne -e ssl:443:privateKey=/cert/key.pem:certKey=/cert/cert.pem ft_transcendence.asgi:application
