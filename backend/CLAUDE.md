# Stack

Backend:

- Python (uv package manager)
- Django 5.2
- Django REST Framework, django-filter
- Django Tenants
- Celery

Database:

- PostgreSQL

Testing:

- pytest
- pytest-django

# Django/Python Rules

1. Always add Django apps inside apps directory
2. Model First Development, Database schema must be designed first. Never create API endpoints before models.

- **Order:**
  - models.py
  - serializers.py
  - services.py
  - views.py
  - urls.py

3. API Design use:

- ViewSets
- Serializers
- Service Layer

Business logic must NOT live in views.

4. Python Method Limits

- **Functions:**
  - max 40 lines

- **Classes:**
  - max 200 lines

Complex logic must move to services.

5. Serializer Rules

- validate all external inputs
- avoid business logic
- only handle transformation

6. Naming Conventions

- snake_case

7. Folder Structure

Follow the standard Django app layout under `backend/apps/`. The apps listed below are examples, NOT an exhaustive list. Create new apps when needed.

8. Creating New Django Apps

Create a new app when the feature has its own models not closely related to existing apps.

- **Steps:**
  1. Create `backend/apps/<app_name>/` with: `__init__.py`, `apps.py`, `models.py`, `serializers.py`, `views.py`, `urls.py`, `services.py`, `admin.py`, `tests
/`, `migrations/`
  2. Register in `config/settings/base.py` → `SHARED_APPS` or `TENANT_APPS` based on whether data is per-tenant or global (refer django-tenants docs)
  3. Wire URLs in `config/urls.py` under `api/v1/<app_name>/`
  4. Run migrations: `uv run manage.py makemigrations` then `uv run manage.py migrate_schemas`

9. Quality Rules

- Always enforce:
  - SOLID principles
  - DRY
  - small functions
  - explicit naming

- Never:
  - duplicate logic
  - mix business logic with controllers
  - skip tests

10. On Model Changes

# 1. Change models
# 2. Create migrations
- uv run manage.py makemigrations

# 3. Apply everywhere
- uv run manage.py migrate_schemas

11. Performance Rules

- Avoid:
  - N+1 queries
  - unnecessary renders
  - large components

- Use:
  - select_related
  - prefetch_related

# Forbidden Areas

Claude must never edit:

node_modules/
.git/
.env

Claude must never manually edit migration files, but may generate them via `makemigrations`.

# Commands

- Backend:
  - uv run pytest
  - uv run manage.py runserver 0:8000


# Testing Protocol
Always follow this 3-phase strategy before declaring tests pass or fail.
Always run in order. Never skip phases.

1. **Smoke:** `uv run pytest -x -q --tb=no`
   - Pass → DONE ✓
   - Fail → go to step 2

2. **Isolate:** `uv run pytest --tb=line -q | grep FAILED` → run each node individually:
   `uv run pytest <node_id> -v --tb=short -s`
   **One at a time**, never batched. Report each before moving on.
   If still failing → continue debugging in step 2
   After fixes: `uv run pytest --lf -v --tb=short` → if clean, go to step 3

3. **Full:** `uv run pytest -v --tb=short`
   Confirms fixes didn't break previously passing tests.
   Only mark complete after this passes.

This is the full suite run. Only report overall success once this passes cleanly.

## Quick Flag Reference

| Flag | Purpose |
|------|---------|
| `-x` | Stop on first failure |
| `-q` | Quiet output |
| `-v` | Verbose (show each test name) |
| `-s` | Show stdout / print output |
| `--tb=no/line/short/long` | Traceback verbosity |
| `--lf` | Re-run only last failed tests |
| `--ff` | Run failed tests first, then rest |
| `-k "name"` | Filter tests by name/keyword |
| `--co` | Dry-run: collect and list tests only |

# Important Rule

Claude must always:

1. Read PRD
2. Write tests
3. Implement minimal code
4. Pass tests
5. Log changes
