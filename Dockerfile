FROM python:3.12.10-slim AS build

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ARG PIP_INDEX_URL
RUN pip install 'uv==0.7.20'
RUN apt-get update && apt-get upgrade --yes \
    && apt-get install --no-install-recommends --yes \
    postgresql=15+* libpq-dev=15.* gnupg=2.2.40-* build-essential=12.9

# DEV Build
FROM build AS dev

EXPOSE 8000

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
RUN uv sync --frozen --no-install-project --quiet

CMD ["uv", "run","python", "manage.py", "runserver", "0.0.0.0:8000"]


# Non-dev build
FROM docker/library/node:18.20-slim AS static

COPY csfeer/package.json csfeer/package-lock.json ./app/csfeer/ 
COPY csfeer/styles ./app/csfeer/styles
COPY csfeer/build-sass.js ./app/csfeer/
WORKDIR /app/csfeer
RUN npm i
RUN npm run build:sass:prod

FROM build AS app-build

RUN apt-get update && apt-get install --no-install-recommends --yes libpq-dev=15.* \
    && apt-get autoremove -y && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Create python user and group in app-build stage
RUN groupadd -g 10001 python && \
    useradd -r -u 10001 -g python python

WORKDIR /app
COPY pyproject.toml uv.lock ./
ARG UV_INDEX_CODEARTIFACT_PASSWORD UV_INDEX_CODEARTIFACT_USERNAME
RUN uv sync --frozen --no-install-project --quiet --no-dev
ENV PATH="/app/.venv/bin:$PATH"
COPY --chown=python:python ./csfeer .
COPY --chown=python:python --from=static /app/csfeer/node_modules /app/node_modules
COPY --chown=python:python --from=static /app/csfeer/static /app/static
RUN python manage.py collectstatic --noinput

# Prod
FROM docker/library/python:3.12.10-slim AS app

RUN apt-get update && apt-get upgrade --yes \
    && apt-get autoremove -y && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN rm -rf /usr/bin/apt-get

RUN groupadd -g 10001 python && \
    useradd -r -u 10001 -g python python

RUN mkdir /app && chown python:python /app
WORKDIR /app

COPY --chown=python:python ./csfeer .
COPY --chown=python:python --from=app-build /app/.venv /app/.venv
USER python

ENV UVLOOP_DISABLE=1
ENV PATH="/app/.venv/bin:$PATH"
CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "csfeer.wsgi:application"  ]


FROM nginxinc/nginx-unprivileged:stable-alpine3.21-perl AS serve-static

COPY --from=app-build /app/staticfiles /usr/share/nginx/html/static
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Switch to user 10001
USER 10001



EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]