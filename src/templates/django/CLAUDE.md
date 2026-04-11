# Stack

Backend:

- Python (uv package manager)
- Django 5.2
- Django REST Framework, django-filter
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

Follow the standard Django app layout under `backend/apps/`.

Refer [django-directory-structure.md](django-directory-structure.md) for the base pattern. The apps listed there are examples, NOT an exhaustive list. Create new apps when needed.

8. Creating New Django Apps

Create a new app when the feature has its own models not closely related to existing apps.

- **Steps:**
  1. Create `backend/apps/<app_name>/` with: `__init__.py`, `apps.py`, `models.py`, `serializers.py`, `views.py`, `urls.py`, `services.py`, `admin.py`, `tests/`, `migrations/`
  2. Wire URLs in `config/urls.py` under `api/v1/<app_name>/`
  3. Run migrations: `uv run python manage.py makemigrations` then `uv run python manage.py migrate`

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

10. After Model Changes

Always run:
- `uv run manage.py makemigrations`
- `uv run manage.py migrate`

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
  - uv run python runserver

# Testing Protocol

Claude must always follow this 3-phase strategy before declaring tests pass or fail. Never skip phases.

## Phase 1 — Smoke Check (always run first)

```bash
uv run pytest -x -q --tb=no
```

- `-x` stops at the first failure immediately
- `-q` keeps output minimal
- `--tb=no` suppresses tracebacks — only pass/fail signal matters here

**Decision:**
- All pass → proceed to Phase 3
- Any fail → proceed to Phase 2

## Phase 2 — Isolate & Debug Failures (only if Phase 1 fails)

First, collect all failing test node IDs:

```bash
uv run pytest --tb=line -q 2>&1 | grep "FAILED"
```

This outputs node IDs like:
```
tests/test_auth.py::test_login_invalid
tests/test_db.py::test_connection_timeout
```

Then run each failing test **one at a time**, never batched:

```bash
uv run pytest <failed_test_node_id> -v --tb=short -s
```

- `-v` shows the full test name
- `--tb=short` gives a concise traceback
- `-s` disables output capture so print statements are visible

Report the result of each test before moving to the next. Do not batch failures together.

**After fixing**, use `--lf` to re-run only the previously failed tests:

```bash
uv run pytest --lf -v --tb=short
```

- If all previously failed tests now pass → proceed to Phase 3
- If still failing → continue debugging in Phase 2

## Phase 3 — Comprehensive Run (only if Phase 1 or Phase 2 fully passes)

```bash
uv run pytest -v --tb=short
```

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

1. Read PRD/Plan
2. Write tests
3. Implement minimal code
4. Run Phase 1 smoke check (`uv run pytest -x -q --tb=no`)
5. If smoke check fails → run Phase 2 (isolate failures one by one)
6. If smoke check passes → run Phase 3 (comprehensive run)
7. Only mark work complete after Phase 3 passes
8. Log changes
