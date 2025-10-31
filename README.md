

## Local Setup


For open id redirection to work correctly, you'll need to add the following entry
to your `/etc/hosts` file:

  ```
  127.0.0.1       oauth.csfeer
  127.0.0.1       ui.csfeer
  ```

After that, with the default settings, you should be able to run the app:

  ```
  docker-compose build
  docker-compose up
  ```

## Using uv for Django commands

You can run Django management commands with uv, which installs dependencies from `pyproject.toml` on demand.

Examples (fish shell):

```fish
# Run system checks
uv run python manage.py check

# Make migrations for the forms app
uv run python manage.py makemigrations form_manager

# Collect static files
uv run python manage.py collectstatic --noinput

# Start the dev server
uv run python manage.py runserver 0.0.0.0:8000
```

Note: `migrate` requires a reachable PostgreSQL database as configured in `csfeer/config.py`.
