# CSFEER Application Architecture Overview

This document provides a high-level overview of the CSFEER (Community Services Form Engine) application architecture, focusing on user authentication via login.gov (Keycloak mock in development) and form data export capabilities.

## System Architecture Flow

```mermaid
flowchart TB
 subgraph AuthProvider["🔐 Authentication Provider"]
    direction TB
        LoginGov["Login.gov<br>(Production)"]
        Keycloak["Keycloak<br>(Development Mock)"]
  end
 subgraph Frontend["Frontend Layer"]
        UI["Django Templates<br>+ USWDS Components<br>+ Django Cotton"]
  end
 subgraph Auth["Authentication Layer"]
        OIDCMiddleware["OAuth2 OIDC Middleware<br>oauth2_authcodeflow"]
        AuthBackend["Custom Auth Backend<br>csfeer/auth.py"]
  end
 subgraph AppLogic["Application Logic"]
        FormViews["Form Manager Views<br>form_manager/views.py"]
        APIViews["API Endpoints<br>(Future: REST/GraphQL)"]
  end
 subgraph Data["Data Layer"]
        Models["Django Models"]
        PostgreSQL[("🗄️ PostgreSQL Database")]
  end
 subgraph CSFEERApp["🏛️ CSFEER Application"]
    direction TB
        Frontend
        Auth
        AppLogic
        Data
  end
    User["👤 User"] -- "1 Access Application" --> UI
    UI -- "2 Redirect to OAuth" --> OIDCMiddleware
    OIDCMiddleware -- "3 OIDC Authorization Flow" --> AuthProvider
    AuthProvider -- "4 Return ID Token + Roles" --> OIDCMiddleware
    OIDCMiddleware -- "5 Create/Update Django User" --> AuthBackend
    AuthBackend -- "6 Assign Groups & Permissions" --> Models
    Models --> PostgreSQL & PostgreSQL
    AuthBackend -- "7 Authenticated Session" --> UI
    UI -- "8 User Interacts" --> FormViews
    FormViews -- "9 CRUD Operations" --> Models
    FormViews -- "10 Form Submission" --> Models
    Models -- "11 Store JSON Data" --> PostgreSQL
    APIViews -. "12 Query Form Data" .-> PostgreSQL
    APIViews -. "13 Export via API" .-> ExternalSystem["🌐 External Service<br>(Data Consumer)"]

    %% Styling
    classDef userStyle fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef authStyle fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef appStyle fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef dataStyle fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef futureStyle stroke-dasharray: 5 5,stroke:#666
    
    class User,ExternalSystem userStyle
    class AuthProvider,OIDCMiddleware,AuthBackend authStyle
    class UI,FormViews,APIViews appStyle
    class Models,PostgreSQL dataStyle
    class APIViews,ExternalSystem futureStyle
```