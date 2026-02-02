#!/bin/bash
set -e

echo "=== CSFeer Startup Script ==="

# Wait for database to be ready
echo "1. Waiting for database connectivity..."
max_attempts=30
attempt=0

until pg_isready -h "$DB_CONFIG__PGHOST" -p "$DB_CONFIG__PGPORT" -U "$DB_CONFIG__PGUSER" -d "$DB_CONFIG__PGDATABASE" -t 1; do
  attempt=$((attempt + 1))
  if [ $attempt -ge $max_attempts ]; then
    echo "❌ Database not ready after $max_attempts attempts"
    echo "Database configuration:"
    echo "  Host: $DB_CONFIG__PGHOST"
    echo "  Port: $DB_CONFIG__PGPORT"
    echo "  Database: $DB_CONFIG__PGDATABASE"
    echo "  User: $DB_CONFIG__PGUSER"
    exit 1
  fi
  echo "   Waiting for database... (attempt $attempt/$max_attempts)"
  sleep 2
done
echo "✅ Database is ready"

# Run migrations
echo "2. Running database migrations..."
if python manage.py migrate --noinput; then
    echo "✅ Migrations complete"
else
    echo "❌ Migrations failed"
    exit 1
fi

# Load forms (idempotent - safe to run multiple times)
echo "3. Loading form definitions..."
if python manage.py load_initial_forms 2>/dev/null; then
    echo "✅ Form definitions loaded"
else
    echo "⚠️  Form loading failed or skipped (may already exist)"
    # Don't exit - forms may already be loaded
fi

# Start application
echo "4. Starting application..."
exec "$@"
