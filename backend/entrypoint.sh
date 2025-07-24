#!/bin/bash

echo "⏳ Waiting for PostgreSQL to be ready..."

while ! nc -z "db" 5432; do
  sleep 1
done

echo "✅ PostgreSQL is up - running migrations..."
flask db upgrade

echo "🚀 Starting Flask app..."
exec flask run --host=0.0.0.0 --port=5000
exec "celery -A app.celery worker --loglevel=info"