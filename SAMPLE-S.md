# Stack
Python (uv), Django 5.2, DRF, django-filter, Django Tenants, Celery, PostgreSQL, pytest, pytest-django

# Rules
- Apps go in `backend/apps/`
- Model-first: models → serializers → services → views → urls
- Business logic in services only, never views
- Functions ≤ 40 lines, Classes ≤ 200 lines
- Serializers: validate inputs, no business logic, transformation only
- snake_case everywhere
- SOLID, DRY, no duplicate logic, no skipped tests

# New App Checklist
1. Create `backend/apps/<name>/` with: `__init__.py apps.py models.py serializers.py views.py urls.py services.py admin.py tests/ migrations/`
2. Register in `config/settings/base.py` → `SHARED_APPS` or `TENANT_APPS`
3. Wire in `config/urls.py` → `api/v1/<name>/`
4. `uv run python manage.py makemigrations && uv run python manage.py migrate`

# After Model Changes
`uv run python manage.py makemigrations && uv run python manage.py migrate`

# Never Touch
`node_modules/` `.git/` `.env/` migration files (generate only, never edit)

# Testing Protocol
Always run in order. Never skip phases.

1. **Smoke:** `uv run pytest -x -q --tb=no`
   - Pass → go to step 3
   - Fail → go to step 2

2. **Isolate:** `uv run pytest --tb=line -q | grep FAILED` → run each node individually:
   `uv run pytest <node_id> -v --tb=short -s`
   One at a time. Report each before moving on.
   After fixes: `uv run pytest --lf -v --tb=short` → if clean, go to step 3

3. **Full:** `uv run pytest -v --tb=short`
   Only mark complete after this passes.

# Workflow
1. Read PRD → 2. Write tests → 3. Implement → 4. Run testing protocol → 5. Log changes
