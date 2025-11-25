# Form Manager API

REST API built with Django Ninja for accessing form data. **Read-only (GET) endpoints.**

## Quick Start

**Interactive docs:** `http://localhost:8000/api/v1/docs`

## Structure

```
api/
├── __init__.py       # Exports the api object
├── endpoints.py      # GET endpoints only
├── schemas.py        # Pydantic response schemas
└── README.md         # This file
```

## Authentication

Uses **Django session authentication**. Must login via web first.

### How to Use

**In Browser (after login):**
```javascript
fetch('/api/v1/forms/definitions', { credentials: 'include' })
  .then(r => r.json())
  .then(console.log);
```

**From External Client:**
1. Login at `/oidc/login` in browser
2. Get `sessionid` from DevTools → Application → Cookies
3. Use in requests:

```bash
curl http://localhost:8000/api/v1/forms/definitions \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

```python
import requests
session = requests.Session()
session.cookies.set('sessionid', 'YOUR_SESSION_ID')
response = session.get('http://localhost:8000/api/v1/forms/definitions')
```

## Alternative: Token Authentication

For programmatic access without browser login, implement token auth:

```python
# Add to endpoints.py
from ninja.security import HttpBearer
from rest_framework.authtoken.models import Token

class TokenAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None

# Update API
api = NinjaAPI(auth=[django_auth, TokenAuth()])  # Accept both
```

Then use:
```bash
curl http://localhost:8000/api/v1/forms/definitions \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Development

- API registered at `/api/v1/` in `csfeer/urls.py`
- Self-documented via Swagger at `/api/v1/docs`
- OpenAPI schema at `/api/v1/openapi.json`
