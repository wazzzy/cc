# Folder Structure

```
backend/
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── celery.py
├── apps/
│   ├── tenants/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── signals.py
│   │   ├── tasks.py
│   │   ├── permissions.py
│   │   ├── admin.py
│   │   ├── tests/
│   │   └── migrations/
│   ├── documents/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── tests/
│   │   └── migrations/
│   └── usage/
│       ├── __init__.py
│       ├── admin.py
│       ├── tests/
│       └── migrations/
│
├── core/
│   ├── middleware/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── permissions.py                # Base permission classes shared across apps
│   ├── pagination.py                 # Standard pagination configs
│   ├── exceptions.py                 # Custom exception classes + DRF exception handler
│   ├── renderers.py                  # Consistent API response format
│   ├── throttling.py                 # Throttle classes
│   ├── models.py                     # Abstract bases: TimestampedModel
│   ├── utils.py                      # Small shared helpers, if large else create a utils dir
│   └── tests/
│
├── integrations/
│   ├── __init__.py
│   ├── keycloak/                     # External client like keycloak
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── config.py
│   ├── prefect/                      # Prefect client
│   │   ├── __init__.py
│   │   ├── client.py
│   └── notifications/                # Email, Slack, webhook
│       ├── __init__.py
│       ├── client.py
│       └── config.py
│
├── conftest.py                       # Shared pytest fixtures: tier, tenant, public_tenant
├── .env.example
├── manage.py
├── pyproject.toml
├── README.md
└── uv.lock
frontend
└── ...
supervisor_logs
└── ...
```
