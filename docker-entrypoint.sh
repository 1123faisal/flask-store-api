#!/bin/bash
set -e

uv run flask --app py_rest_api db upgrade
exec uv run --no-dev gunicorn --bind 0.0.0.0:${PORT:-5000} --access-logfile - --error-logfile - 'py_rest_api:create_app()'