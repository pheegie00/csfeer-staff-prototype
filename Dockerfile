FROM docker.io/library/python:3.12.13-slim-trixie AS build-base
# The base build target should only include the resources necessary
# for running the app in a production environment, i.e. no
# tests or other tooling.

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV UVLOOP_DISABLE=1

ARG VERSION=local

# Install os dependencies
RUN pip install 'uv==0.7.20'
RUN apt-get update && apt-get upgrade --yes \
    && apt-get install --no-install-recommends --yes \
    postgresql libpq-dev gnupg build-essential curl \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-xlib-2.0-0 \
    && apt-get autoremove -y && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Create an application user
RUN groupadd -g 10001 python && \
    useradd -u 10001 -g python python
RUN mkdir -m 700 -p /home/python && chown python:python /home/python

# Create an app directory owned by the python user
RUN mkdir -m 700 /app && chown python:python /app

WORKDIR /app

# Copy Django project apps and other application code
COPY --chown=python:python ./csfeer /app/csfeer
COPY --chown=python:python ./core /app/core
COPY --chown=python:python ./django_cotton_uswds /app/django_cotton_uswds
COPY --chown=python:python ./form_manager /app/form_manager
COPY --chown=python:python ./users /app/users
COPY --chown=python:python ./pyproject.toml .
COPY --chown=python:python ./uv.lock .
COPY --chown=python:python ./manage.py .

RUN echo $VERSION >> /app/.version

# Create logs directory for Django logging
RUN mkdir -p /app/logs && chown python:python /app/logs

# Set the user to python
USER python

# Install python dependencies
RUN uv sync --frozen --no-install-project

# Add the virtual environment executables to the PATH
ENV PATH="/app/.venv/bin:$PATH"


##### Staticfiles build
FROM docker.io/library/node:18.20-slim AS static

WORKDIR /app
COPY . /app
RUN npm i
RUN npm run build


##### Development build
FROM build-base AS dev

EXPOSE 8000

WORKDIR /app

COPY --chown=python:python --from=static /app/frontend/built /app/csfeer/static/frontend
RUN uv run manage.py collectstatic --noinput

USER root

RUN playwright install-deps chromium \
    && apt-get autoremove -y && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

USER python

RUN playwright install chromium

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000", "--nostatic"]

##### Production build
FROM build-base AS prod

COPY --chown=python:python --from=static /app/frontend/built /app/csfeer/static/frontend
RUN uv run manage.py collectstatic --noinput

CMD [ "gunicorn", "--user", "python", "--bind", "0.0.0.0:8000", "csfeer.wsgi:application"]

##### Production e2e test runner
FROM prod AS prod-e2e
USER root
RUN /app/.venv/bin/playwright install-deps chromium \
    && apt-get autoremove -y && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
USER python
RUN /app/.venv/bin/playwright install chromium