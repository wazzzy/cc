# Stack
Python (uv), Django 5.2, DRF, django-filter, Django Tenants, Celery, PostgreSQL, pytest, pytest-django

# Rules
- Functions ≤ 40 lines, Classes ≤ 200 lines
- snake_case everywhere
- SOLID, DRY, no duplicate logic, no skipped tests

# Never Touch
`node_modules/` `.git/` `.env` migration files (generate only, never edit)

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

## Context Rules (STRICT)
* Never read the same file twice
* If a file was already read, reuse that content
* Read only what is necessary (avoid full files)
* If you are re-reading files, consider referencing earlier reads. Use offset/limit for large files.
* Expand context only when required
* Use Grep instead of Read for searching

Before any file read:
Ask: "Do I already have this?"
If yes → reuse
If partial → extend, don’t reload
