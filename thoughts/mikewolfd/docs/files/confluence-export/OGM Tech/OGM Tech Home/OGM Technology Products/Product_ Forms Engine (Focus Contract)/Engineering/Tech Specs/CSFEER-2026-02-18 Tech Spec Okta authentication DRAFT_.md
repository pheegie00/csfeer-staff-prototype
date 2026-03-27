
[OGM Technology Products](../../../../OGM%20Technology%20Products.md) > [Product: Forms Engine (Focus Contract)](../../../Product_%20Forms%20Engine%20(Focus%20Contract).md) > [Engineering](../../Engineering.md) > [Tech Specs](../Tech%20Specs.md)

# CSFEER-2026-02-18 Tech Spec Okta authentication DRAFT:

|                 |                                                                  |
|:----------------|:-----------------------------------------------------------------|
| **Author**      | Mohammad Taleb                                                   |
| **Date**        | 2026-02-18 <br/>                                                 |
| **Reviewed by** |                                                                  |
| **Status**      | **→ Draft** <br/> Ready for review <br/> Approved <br/> Deferred |

## Table of Contents:

- [Table of Contents:](#table-of-contents)
- [Overview](#overview)
- [acf.okta.org](#acf-okta-org)
- [Goals and Product Requirements](#goals-and-product-requirements)
- [Assumptions](#assumptions)
- [Out of Scope](#out-of-scope)
- [Open Questions](#open-questions)
- [Approach](#approach)
  - [Redirect authentication](#redirect-authentication)
  - [Stack](#stack)
  - [OIDC Authorization Code Flow (Confidential Client + PKCE)](#oidc-authorization-code-flow-confidential-client-pkce)
  - [Middleware Stack](#middleware-stack)
  - [Role Mapping](#role-mapping)
  - [OIDC Configuration (from csfeer/config.py)](#oidc-configuration-from-csfeer-config-py)
  - [User Identity](#user-identity)
  - [Sign-Out](#sign-out)
  - [Other Options Considered](#other-options-considered)
- [Schema Changes](#schema-changes)
- [Security and Privacy](#security-and-privacy)
- [Test Plan](#test-plan)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
  - [E2E Tests (Playwright — existing)](#e2e-tests-playwright-existing)
  - [QA / Manual Test Plan](#qa-manual-test-plan)
- [Deployment and Rollout](#deployment-and-rollout)
- [Rollback Plan](#rollback-plan)
- [Monitoring and Logging](#monitoring-and-logging)
- [Metrics](#metrics)
- [Long-term Support](#long-term-support)
- [Timeline](#timeline)

## Overview

This spec documents the authentication design for the **CSFEER** application. Authentication is handled via **OpenID Connect (OIDC)** using the **Redirect (Okta-hosted) deployment model** in production, with **Okta** (`acf.okta.com`) as the Identity Provider (IdP). In non-production environments where Okta is unavailable, **Keycloak** is used as a fully OIDC-compliant mock IdP, providing identical behavior.

The production target is to integrate with **[Login.gov](http://Login.gov)** via Okta as the upstream IdP, following ACF/DOS standards.

CSFEER is a **Django server-rendered web application** using the [`oauth2_authcodeflow`](https://pypi.org/project/django-oauth2-authcodeflow/) library to implement the **Authorization Code Flow with PKCE + Client Secret** (`force_secret_with_pkce = true`). All token handling occurs server-side; the browser receives only a Django session cookie.

**Reference:** [Okta Redirect vs. Embedded Authentication](https://developer.okta.com/docs/concepts/redirect-vs-embedded/#redirect-authentication)

## ![](/download/attachments/182917375/Screenshot%202026-02-19%20at%2011.31.16%E2%80%AFAM.png?version=1&modificationDate=1771518752162&api=v2)acf.okta.org

## Goals and Product Requirements

- Enable secure, standards-based user authentication for CSFEER using OIDC.
- Delegate credential management and MFA to Okta/[Login.gov](http://Login.gov), reducing CSFEER's security surface area.
- Map OIDC roles from the IdP to Django groups and permissions automatically on each login.
- Support SSO via the Okta session across other ACF-integrated applications.
- Maintain environment parity between local development (Keycloak) and production (Okta/[Login.gov](http://Login.gov)).

## Assumptions

- The Okta org at `acf.okta.com` is provisioned and an OIDC client (`csfeer-auth`) is or will be registered there, matching the client ID used in the Keycloak mock.
- The application uses a **confidential client** with `force_secret_with_pkce = true` — both a client secret and PKCE are required.
- The OIDC discovery document is the single source of truth for endpoint configuration; no endpoints are hardcoded.
- Users are provisioned in the IdP. CSFEER auto-provisions Django users on first login using the `email` claim as the primary identifier.
- Roles are conveyed via the `realm_access.roles` claim in the JWT (Keycloak convention). The Okta/[Login.gov](http://Login.gov) token must be configured to emit a structurally equivalent claim for this mapping to work without code changes.
- All tokens are held server-side; the browser only receives a Django session cookie.
- Session/token lifetimes are governed by IdP policy: access token 5 min, session idle 30 min, session max 10 hours (based on Keycloak config).

## Out of Scope

- User provisioning / deprovisioning into Okta (owned by IT/Okta Admin team).
- MFA configuration and policy management (owned by Okta Admin team).
- Embedded authentication or direct API authentication flows.
- SAML-based SSO.
- Authorization (role/permission logic within CSFEER beyond the authenticated identity).
- Building a custom sign-in UI.

## Open Questions

|   # | Question                                                                                                                                                                                                              | Owner                    | Status                                        |
|----:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------|:----------------------------------------------|
|   1 | Will the Okta/[Login.gov](http://Login.gov) token emit roles in a `realm_access.roles` structure, or will the `extend_user_with_roles` backend need to be updated to map a different claim?                           | Engineering / Okta Admin | **Critical — must resolve before production** |
|   2 | What is the registered `redirect_uri` in the production Okta app registration? Must match the Django OIDC callback URL (`/oidc/callback`).                                                                            | DevOps / Okta Admin      | Open                                          |
|   3 | Will a custom Okta Authorization Server be used? If so, the discovery document URL changes from `acf.okta.com/.well-known/openid-configuration` to `acf.okta.com/oauth2/{serverId}/.well-known/openid-configuration`. | Okta Admin               | Open                                          |
|   4 | Are the scopes `openid`, `email`, `profile`, `roles`, and `offline_access` all supported and approved in the production Okta org?                                                                                     | Okta Admin               | Open                                          |
|   5 | Post-logout redirect URL for production — where should users land after signing out?                                                                                                                                  | Product / Engineering    | Open                                          |
|   6 | Will `refresh_token` (`offline_access` scope) be enabled in the production Okta client? Required for the `RefreshAccessTokenMiddleware` and `RefreshSessionMiddleware` to function.                                   | Okta Admin               | Open                                          |

  

## Approach

### Redirect authentication

The user or system is redirected to Okta for credential verification. The user or system is then provided authenticated access to the client app and other Service Providers. When a user signs in to the client app, they're redirected to Okta using a protocol like SAML or **OpenID Connect**. After the user signs in (based on policies configured in Okta), Okta redirects the user back to your app.

![](/download/attachments/182917375/redirect-auth-seq-flow.png?version=1&modificationDate=1771440195302&api=v2)

### Stack

| Component            | Implementation                                                         |
|:---------------------|:-----------------------------------------------------------------------|
| Language / Framework | Python / Django                                                        |
| OIDC Library         | `oauth2_authcodeflow`                                                  |
| Auth Backend         | `csfeer.backends.EmailOIDCAuthenticationBackend`                       |
| Role Extension Hook  | `csfeer.backends.extend_user_with_roles`                               |
| IdP (Production)     | Okta (`acf.okta.com`) → [Login.gov](http://Login.gov) upstream         |
| IdP (Development)    | Keycloak (`oauth.csfeer:8081`), realm: `csfeer`, client: `csfeer-auth` |

### OIDC Authorization Code Flow (Confidential Client + PKCE)

Because `OIDC_RP_FORCE_SECRET_WITH_PKCE = true`, CSFEER uses both a client secret and PKCE — the most secure configuration for a confidential server-side client:

1. User accesses a protected route. The `LoginRequiredMiddleware` intercepts unauthenticated requests.
2. The server generates a `state`, `nonce`, `code_verifier`, and `code_challenge`, stores them in the Django session, and redirects the browser to the IdP's authorization endpoint (resolved via the OIDC discovery document).
3. The user authenticates at the Okta-hosted (or Keycloak) sign-in page.
4. The IdP redirects back to `/oidc/callback` with an authorization `code` and `state`.
5. The server validates `state`, then exchanges the `code` + `code_verifier` + client secret for an **ID token**, **access token**, and **refresh token** via a server-to-server call to the IdP's token endpoint.
6. The ID token is validated (JWKS signature, `iss`, `aud`, `exp`, `nonce`).
7. `EmailOIDCAuthenticationBackend.get_or_create_user()` looks up or auto-provisions a Django user by `email` claim.
8. `extend_user_with_roles()` is called to sync Django groups and staff/superuser status from the `realm_access.roles` JWT claim.
9. The `oidc_user_id` (`sub` claim) is persisted to `UserProfile`.
10. A Django session is created; a secure session cookie is issued to the browser.

### Middleware Stack

The following middleware is active in order:

```
SessionMiddleware
LoginRequiredMiddleware        ← enforces auth on all routes except excluded patterns
RefreshAccessTokenMiddleware   ← silently refreshes access token using refresh token
RefreshSessionMiddleware       ← extends Django session on token refresh
```

**Excluded URL patterns** (no auth required): `api/`, `logged-out`

### Role Mapping

Roles from the IdP JWT (`realm_access.roles`) are mapped to Django groups on every login:

| JWT Role       | Django Effect                                            |
|:---------------|:---------------------------------------------------------|
| `csfeer_admin` | `is_staff = True`, `is_superuser = True`, added to group |
| `csfeer_staff` | `is_staff = True`, added to group                        |
| `superuser`    | `is_superuser = True`, added to group                    |
| Any other role | Django group created/assigned by name                    |

Existing group memberships are **cleared on every login** and re-synced from the token.

### OIDC Configuration (from `csfeer/config.py`)

| Setting                          | Value                                                                                                      |
|:---------------------------------|:-----------------------------------------------------------------------------------------------------------|
| `OIDC_RP_CLIENT_ID`              | `csfeer-auth`                                                                                              |
| `OIDC_RP_CLIENT_SECRET`          | Injected from environment (`OIDC_CONFIG__CLIENT_SECRET`)                                                   |
| `OIDC_RP_FORCE_SECRET_WITH_PKCE` | `true`                                                                                                     |
| `OIDC_RP_SCOPES`                 | `openid`, `email`, `profile`, `roles`, `offline_access`                                                    |
| Discovery URL (dev)              | `http://oauth.csfeer:8081/realms/csfeer/.well-known/openid-configuration`                                  |
| Discovery URL (prod)             | `https://acf.okta.com/.well-known/openid-configuration` *(or custom auth server URL — see Open Questions)* |

### User Identity

- Primary identifier: **email** (not `sub` / username).
- The Okta `sub` claim is stored in `UserProfile.oidc_user_id` for audit/correlation purposes.
- On first login, a personal `OrganizationProfile` and `UserOrganizationMembership` (role: `admin`) are auto-created for the user.

### Sign-Out

Sign-out clears the Django session and redirects to the IdP's logout endpoint (RP-Initiated Logout) to also terminate the Okta SSO session. The post-logout redirect destination is TBD (see Open Questions).

### Other Options Considered

**Embedded authentication:** Rejected in favor of the redirect model — offloads credential and MFA handling entirely to Okta/[Login.gov](http://Login.gov), reduces XSS risk, and is the Okta-recommended approach. SSO across ACF applications is also handled automatically.

## Schema Changes

The following database changes are already implemented and captured in migrations:

- **`users_userprofile`** table includes `oidc_user_id` (VARCHAR 255, nullable, unique) — stores the `sub` claim from the OIDC token for cross-referencing with the IdP.
- **`auth_group`** rows are created dynamically on first login for any new role name found in the JWT. No schema change required, but ops should be aware these are auto-generated.
- No additional schema changes are required for the Okta integration specifically.

## Security and Privacy

- **Token validation:** ID token signature validated via IdP JWKS; `iss`, `aud`, `exp`, and `nonce` claims all validated by `oauth2_authcodeflow`.
- **PKCE + client secret (`force_secret_with_pkce`):** Dual protection — PKCE mitigates authorization code interception; client secret authenticates the server-to-server token exchange.
- **State parameter:** Generated per-request, validated on callback to prevent CSRF.
- **Nonce:** Included in the authorization request and validated in the ID token to prevent replay attacks.
- **Token storage:** Tokens are never sent to the browser. The browser receives only a Django `sessionid` cookie (HttpOnly, Secure, `SameSite` per Django defaults).
- **Client secret:** Must never be hardcoded. Injected at runtime via environment variable `OIDC_CONFIG__CLIENT_SECRET`; must be stored in a secrets manager (e.g., AWS Secrets Manager) in production.
- **Redirect URI allowlisting:** Exact-match redirect URIs must be registered in the Okta app configuration.
- **Transport security:** All IdP communication over HTTPS/TLS in production. (Keycloak dev instance uses HTTP on localhost only — `127.0.0.1:8081`.)
- **PII:** `email`, `name`, and `sub` received from the IdP are PII and stored in the database. Data handling must comply with ACF data policies.
- **Group auto-creation:** Roles in JWT that don't exist as Django groups are created automatically. Ensure Okta token claims are controlled to prevent privilege escalation via unexpected role names.

## Test Plan

### Unit Tests

- `EmailOIDCAuthenticationBackend.get_or_create_user()` — user lookup by email, auto-provisioning on first login.
- `extend_user_with_roles()` — role-to-group mapping, `is_staff` / `is_superuser` assignment, group clearing, `UserProfile.oidc_user_id` persistence, org auto-creation.
- Config loading from environment variables.

### Integration Tests

- Full Authorization Code Flow against the Keycloak dev mock.
- Callback with valid and invalid `state` / `nonce`.
- Token refresh via `RefreshAccessTokenMiddleware`.
- Sign-out — verify Django session cleared and IdP logout endpoint called.
- Expired access token — verify silent refresh occurs without re-authentication prompt.
- User with no roles — verify no groups assigned, `is_staff = False`.

### E2E Tests (Playwright — existing)

- Admin user login and protected page access (`test_admin_user_login`).
- Demo user login (`test_demo_user_login`).
- Multi-user login/logout cycle (`test_login_with_different_users`).
- Role-based access control on protected views.

### QA / Manual Test Plan

- Happy path: login → protected resource → logout.
- Deep link: unauthenticated access to a protected URL → login → redirect back to original URL.
- MFA enforcement (once configured in Okta).
- Session expiry: verify re-authentication prompt after idle timeout.
- SSO: user already signed into another Okta app → CSFEER login without re-entering credentials.
- Invalid/tampered `state` on callback: verify error response, no session created.

## Deployment and Rollout

- **Okta app registration:** Create an OIDC application in `acf.okta.com` for each environment (dev, staging, prod). Client ID should match `csfeer-auth` for environment parity. Record client secret securely.
- **Configuration:** All OIDC settings are environment-variable-driven via `OIDC_CONFIG__*` prefixed vars. No hardcoded values. The discovery document URL is the only value that changes between environments.
- **Secrets management:** `OIDC_CONFIG__CLIENT_SECRET` must be stored in a secrets manager and injected at runtime. Must not appear in `.env` files committed to version control.
- **Rollout order:** Local (Keycloak) → Dev (Okta) → Staging → UAT → Production.
- **Keycloak decommission:** Keycloak remains in place as the local dev mock and is not removed. It is not used in any environment above dev.

## Rollback Plan

- The OIDC discovery URL is the primary configuration switch. Pointing `OIDC_CONFIG__DOCUMENT_URL` back to the previous IdP endpoint and redeploying is sufficient to roll back an IdP change without a code release.
- If a code release must be rolled back, redeploy the previous application version. Okta configuration changes are non-destructive.
- **Watch for:** 401/403 error rates on protected routes; authentication failures in Okta System Log; Django error logs for token validation failures or missing claims (especially `realm_access.roles` or `email`).

## Monitoring and Logging

- **Okta System Log**: Okta provides a full audit log of all authentication events (successful logins, failures, MFA challenges, logouts) accessible via the Admin Console and the Okta Events API.
- **Application logs**: Log authentication lifecycle events (session created, session destroyed, token refresh, auth errors) — **do not log token values or credentials**.
- **Alerting**: Alert on spikes in authentication errors or failed login rates, which may indicate misconfiguration or an attack.
- **Health check**: Include Okta's OIDC discovery endpoint reachability as part of application health monitoring.

## Metrics

- **Login success rate:** % of OIDC callbacks resulting in a valid Django session.
- **Login latency:** Time from redirect to IdP to successful session establishment.
- **Token refresh rate:** Frequency of silent token refreshes (indicates active session usage).
- **Authentication error rate:** Token validation failures, missing claims, invalid `state`/`nonce`.
- **Role sync anomalies:** Logins where `realm_access.roles` is absent or empty (may indicate IdP misconfiguration).

## Long-term Support

- **Ownership:** The CSFEER engineering team owns the OIDC integration and `oauth2_authcodeflow` library updates.
- **Role claim mapping:** If the Okta/[Login.gov](http://Login.gov) token structure differs from the Keycloak `realm_access.roles` convention, `extend_user_with_roles()` in `csfeer/backends.py` must be updated. This is the highest-risk transition point.
- **Client secret rotation:** Establish a rotation schedule and process in the secrets manager.
- **Keycloak realm maintenance:** The `realm.json` must be kept in sync with any Okta scope or client config changes so that local development remains a faithful mock of production.
- **Knowledge transfer:** OIDC app registration details, environment variable names, and the role-mapping logic must be documented for any team onboarding.

## Timeline

| Task                                                               | Owner                | Estimate   |
|:-------------------------------------------------------------------|:---------------------|:-----------|
| Okta OIDC app registration (per environment)                       | Okta Admin / DevOps  |            |
| OIDC client library integration and Authorization Code + PKCE flow | Engineering          |            |
| Token validation logic (JWKS, claims)                              | Engineering          |            |
| Session management (creation, renewal, logout)                     | Engineering          |            |
| Secrets / config management setup                                  | DevOps / Engineering |            |
| Unit and integration test coverage                                 | Engineering          |            |
| QA manual testing (all environments)                               | QA                   |            |
| Staging deployment and UAT                                         | Engineering / QA     |            |
| Production rollout and monitoring                                  | Engineering / DevOps |            |
| **Total**                                                          |                      |            |
