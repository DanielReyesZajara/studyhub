#!/bin/sh
set -eu
python -m scripts.wait_for_db
flask --app wsgi:app db upgrade
exec flask --app wsgi:app run --host=0.0.0.0 --port=5000 --debug
