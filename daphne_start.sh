#!/bin/bash

SCRIPT_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"

cd "$SCRIPT_DIR"

NAME="bingothon-donations"                                   # Name of the application
SOCKFILE="/tmp/donationtracker.sock"
echo "Starting $NAME as `whoami`"

# Activate the virtual environment

source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=settings

exec daphne routing:application \
  --proxy-headers \
  --unix-socket=$SOCKFILE
