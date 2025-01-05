#!/bin/bash

# Exec into the manage to run the workers server, this replaces the shell with the workers process
# ensuring that signals received by the container are captured by the daphne server
echo "Starting workers..."
exec /app/ft_transcendence/manage.py runworker pong_update_channel
