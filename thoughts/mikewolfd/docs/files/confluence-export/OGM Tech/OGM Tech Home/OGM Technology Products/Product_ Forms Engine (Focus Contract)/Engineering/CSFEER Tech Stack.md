
[OGM Technology Products](../../../OGM%20Technology%20Products.md) > [Product: Forms Engine (Focus Contract)](../../Product_%20Forms%20Engine%20(Focus%20Contract).md) > [Engineering](../Engineering.md)

# CSFEER Tech Stack

- [Frontend](#frontend)
- [Backend](#backend)
  - [Django Plugins](#django-plugins)
- [Database & Infrastructure](#database-infrastructure)
  - [Build & Bundling](#build-bundling)
  - [Testing & Dev Tools](#testing-dev-tools)
- [Technical Architecture & Security Framework](#technical-architecture-security-framework)

## Frontend

| Technology    | Version   | Description                                     | Link                                |
|:--------------|:----------|:------------------------------------------------|:------------------------------------|
| **Python**    | 3.12      | Core programming language                       | <https://www.python.org/>           |
| **Django**    | 6.0+      | Web framework                                   | <https://www.djangoproject.com/>    |
| **Alpine.js** | 3.15+     | Lightweight reactive JS framework               | <https://alpinejs.dev/>             |
| **USWDS**     | 3.13+     | U.S. Web Design System (UI components & styles) | <https://designsystem.digital.gov/> |
| **SASS/SCSS** | —         | CSS preprocessor (via sass-loader)              | <https://sass-lang.com/>            |

## Backend

| Technology            | Version   | Description                               | Link                                                                 |
|:----------------------|:----------|:------------------------------------------|:---------------------------------------------------------------------|
| **Python**            | 3.12      | Core programming language                 | <https://www.python.org/>                                            |
| **Django**            | 6.0+      | Web framework                             | <https://www.djangoproject.com/>                                     |
| **Django Ninja**      | 1.4+      | API framework (fast, type-safe REST APIs) | <https://django-ninja.dev/>                                          |
| **Gunicorn**          | 23.0+     | Python WSGI HTTP server (production)      | <https://gunicorn.org/>                                              |
| **Pydantic**          | 2.12+     | Data validation & settings management     | <https://docs.pydantic.dev/>                                         |
| **Pydantic Settings** | 2.11+     | Configuration via environment variables   | <https://docs.pydantic.dev/latest/concepts/pydantic_settings/>       |
| **Boto3**             | 1.40+     | AWS SDK for Python                        | <https://boto3.amazonaws.com/v1/documentation/api/latest/index.html> |
| **WeasyPrint**        | 62.3+     | HTML/CSS to PDF generation                | <https://weasyprint.org/>                                            |
| **Psycopg2**          | 2.9+      | PostgreSQL database adapter               | <https://www.psycopg.org/docs/>                                      |
| **WhiteNoise**        | 6.11+     | Static file serving                       | <https://whitenoise.readthedocs.io/>                                 |
| **phonenumbers**      | 9.0+      | Phone number parsing & validation         | <https://pypi.org/project/phonenumbers/>                             |
| **semver**            | 3.0+      | Semantic versioning utilities             | <https://pypi.org/project/semver/>                                   |

### Django Plugins

| Technology                     | Version   | Description                   | Link                                                   |
|:-------------------------------|:----------|:------------------------------|:-------------------------------------------------------|
| **Django Cotton**              | 2.1+      | Reusable template components  | <https://django-cotton.com/>                           |
| **Django Crispy Forms**        | 2.4+      | Better Django form rendering  | <https://django-crispy-forms.readthedocs.io/>          |
| **Django JSON Widget**         | 2.0+      | JSON editing widget for admin | <https://pypi.org/project/django-json-widget/>         |
| **Django OAuth2 AuthCodeFlow** | 1.3+      | OIDC/OAuth2 authentication    | <https://pypi.org/project/django-oauth2-authcodeflow/> |
| **Django Pattern Library**     | 1.5+      | UI component pattern library  | <https://torchbox.github.io/django-pattern-library/>   |
| **Django NPM**                 | 1.0+      | NPM integration for Django    | <https://pypi.org/project/django-npm/>                 |

## Database & Infrastructure

| Technology        | Description                                     | Link                          |
|:------------------|:------------------------------------------------|:------------------------------|
| **PostgreSQL**    | Relational database                             | <https://www.postgresql.org/> |
| **Docker**        | Containerization                                | <https://www.docker.com/>     |
| **Nginx**         | Reverse proxy / static file server (production) | <https://nginx.org/>          |
| **AWS (S3, IAM)** | Cloud infrastructure & IAM-based DB auth        | <https://aws.amazon.com/>     |

### Build & Bundling

| Technology   | Version   | Description                     | Link                         |
|:-------------|:----------|:--------------------------------|:-----------------------------|
| **Webpack**  | 5.0+      | JavaScript module bundler       | <https://webpack.js.org/>    |
| **Node.js**  | 18.x      | JavaScript runtime (build only) | <https://nodejs.org/>        |
| **uv**       | 0.7+      | Fast Python package manager     | <https://docs.astral.sh/uv/> |

### Testing & Dev Tools

| Technology        | Version   | Description                      | Link                                    |
|:------------------|:----------|:---------------------------------|:----------------------------------------|
| **Pytest**        | —         | Python testing framework         | <https://docs.pytest.org/>              |
| **Pytest-Django** | 4.11+     | Django testing plugin for pytest | <https://pytest-django.readthedocs.io/> |
| **Playwright**    | 1.49+     | End-to-end browser testing       | <https://playwright.dev/python/>        |
| **Ruff**          | 0.9+      | Fast Python linter               | <https://docs.astral.sh/ruff/>          |
| **Black**         | 25.9+     | Python code formatter            | <https://black.readthedocs.io/>         |
| **Pyright**       | 1.1+      | Python type checker              | <https://microsoft.github.io/pyright/>  |
| **Pre-commit**    | 4.0+      | Git hooks framework              | <https://pre-commit.com/>               |
| **Faker**         | 39.0      | Test data generation             | <https://faker.readthedocs.io/>         |
| **FreezeGun**     | 1.5+      | Mock datetime in tests           | <https://github.com/spulec/freezegun>   |

## Technical Architecture & Security Framework

[Technical Architecture & Security Framework](/spaces/OXT/pages/168827066/Technical+Architecture+Security+Framework)
