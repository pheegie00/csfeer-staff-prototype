FROM docker.io/library/python:3.12.13-slim-trixie AS build

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ARG PIP_INDEX_URL
RUN pip install 'uv==0.7.20'
RUN apt-get update && apt-get upgrade --yes \
    && apt-get install --no-install-recommends --yes \
    postgresql libpq-dev gnupg build-essential \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-xlib-2.0-0 \
    && apt-get autoremove -y && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Non-dev build
FROM docker.io/library/node:18.20-slim AS static

WORKDIR /app
COPY . /app
RUN npm i
RUN npm run build


# DEV Build
FROM build AS dev

EXPOSE 8000

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

# Create logs directory for Django logging
RUN mkdir -p /var/log/app && chown appuser:appuser /var/log/app

USER appuser

# Install dependencies (cached if pyproject.toml/uv.lock unchanged)
RUN uv sync --frozen --no-install-project --quiet

COPY --chown=appuser:appuser . /app

RUN uv run python manage.py collectstatic --noinput

CMD ["uv", "run","python", "manage.py", "runserver", "0.0.0.0:8000"]


# E2E test runner - extends dev with Playwright Chromium pre-installed
FROM dev AS e2e-runner
USER root
RUN /app/.venv/bin/playwright install-deps chromium \
    && apt-get autoremove -y && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
USER appuser
RUN /app/.venv/bin/playwright install chromium


FROM build AS app-build

# Create python user and group in app-build stage
RUN groupadd -g 10001 python && \
    useradd -r -u 10001 -g python python

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --quiet
ENV PATH="/app/.venv/bin:$PATH"
COPY --chown=python:python . .
COPY --chown=python:python --from=static /app/node_modules /app/node_modules
COPY --chown=python:python --from=static /app/frontend/built /app/static
RUN mkdir -p /var/log/app && chown python:python /var/log/app
RUN uv run python manage.py collectstatic --noinput

# Prod
FROM docker.io/library/python:3.12.13-slim-trixie AS app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install only runtime dependencies (no build tools)
RUN apt-get update && apt-get upgrade --yes \
    && apt-get install --no-install-recommends --yes \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-xlib-2.0-0 \
    && apt-get autoremove -y && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/bin/apt-get

RUN groupadd -g 10001 python && \
    useradd -r -u 10001 -g python python

RUN mkdir /app && chown python:python /app
WORKDIR /app

COPY --chown=python:python ./csfeer .
COPY --chown=python:python --from=app-build /app/.venv /app/.venv

# Create logs directory for Django logging
RUN mkdir -p /var/log/app && chown python:python /var/log/app

USER python

ENV UVLOOP_DISABLE=1
ENV PATH="/app/.venv/bin:$PATH"
CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "csfeer.wsgi:application"  ]


FROM docker.io/nginxinc/nginx-unprivileged:stable-alpine3.21-perl AS serve-static

COPY --from=app-build /app/staticfiles /usr/share/nginx/html/static
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Switch to user 10001
USER 10001



EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]