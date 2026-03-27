# Plan: ccskills Refactor + CLI Distribution Tool

> Source PRD: docs/prd-ccskills-refactor.md

## Architectural decisions

- **Skill folder naming**: short, lowercase, hyphenated (`write-prd`, `plan-from-prd`, `issues-from-prd`, `interrogate`, `tdd-backend`, `tdd-frontend`)
- **Skill structure**: each skill dir contains `SKILL.md` + supporting `.md` files; no non-markdown files
- **CLI package**: Python, `pyproject.toml`, entry point `ccskills`, no external deps (stdlib only)
- **Install target**: `<cwd>/.claude/skills/<skill-name>/` — local project only
- **Skill discovery**: any top-level dir in the package containing `SKILL.md`
- **Installable via**: `uv tool install git+<repo>` or `uvx`

---

## Phase 1: Rename skills + tighten frontmatter

**User stories**: 10, 11

### What to build

Rename the four non-tdd skill folders to their short canonical names. Update the `name` field in each `SKILL.md` frontmatter to match. Review and tighten the `description` field in each `SKILL.md` to list precise natural trigger phrases that avoid false positives and missed invocations.

Renames:
- `write-a-prd/` → `write-prd/`
- `prd-to-plan/` → `plan-from-prd/`
- `prd-to-issues/` → `issues-from-prd/`
- `grill-me/` → `interrogate/`

### Acceptance criteria

- [ ] All four folders renamed; no old folder names remain
- [ ] Each `SKILL.md` `name` field matches its folder name
- [ ] Each `SKILL.md` `description` field contains precise trigger phrases (no vague or overlapping language)

---

## Phase 2: tdd-frontend split

**User stories**: 1, 3, 4, 13

### What to build

Create `tdd-frontend/` as a complete, self-contained skill. Copy the full philosophy section from `tdd/SKILL.md` verbatim. Bring across `frontend-test.md` and `frontend-mocking.md` unchanged. Extract only the frontend section from `interface-design.md` into `interface-design-frontend.md`. Rename `deep-modules.md` → `deep-modules-frontend.md` and `refactoring.md` → `refactoring-frontend.md`. Update all internal doc links in `tdd-frontend/SKILL.md` to point to the new filenames. Ensure `frontend-test.md` includes RTL + Vitest examples with Next.js App Router patterns and async testing.

### Acceptance criteria

- [ ] `tdd-frontend/SKILL.md` exists with philosophy verbatim from `tdd/SKILL.md`
- [ ] `tdd-frontend/` contains: `frontend-test.md`, `frontend-mocking.md`, `interface-design-frontend.md`, `deep-modules-frontend.md`, `refactoring-frontend.md`
- [ ] `interface-design-frontend.md` contains only the frontend (TypeScript/React) section
- [ ] `frontend-test.md` includes RTL + Vitest examples with Next.js App Router patterns and async testing
- [ ] All internal links in `tdd-frontend/SKILL.md` resolve to files that exist in the same folder
- [ ] No backend content appears in any `tdd-frontend/` file

---

## Phase 3: tdd-backend split + delete tdd/

**User stories**: 2, 3, 5, 6, 7, 8, 9

### What to build

Create `tdd-backend/` as a complete, self-contained skill. Copy the full philosophy section from `tdd/SKILL.md` verbatim. Bring across `backend-test.md` and `backend-mocking.md` unchanged. Extract only the backend section from `interface-design.md` into `interface-design-backend.md`. Create new files: `deep-modules-backend.md` (Django-specific: managers, service classes, utility modules) and `refactoring-backend.md` (Python-specific candidates: long views, fat models, primitive obsession). Update all internal doc links in `tdd-backend/SKILL.md` to point to backend files. Once both new skills are complete and verified, delete the original `tdd/` folder entirely.

### Acceptance criteria

- [ ] `tdd-backend/SKILL.md` exists with philosophy verbatim from `tdd/SKILL.md`
- [ ] `tdd-backend/` contains: `backend-test.md`, `backend-mocking.md`, `interface-design-backend.md`, `deep-modules-backend.md`, `refactoring-backend.md`
- [ ] `interface-design-backend.md` contains only the Django/Python section
- [ ] `deep-modules-backend.md` covers Django managers, service classes, utility modules
- [ ] `refactoring-backend.md` covers long views, fat models, primitive obsession
- [ ] All internal links in `tdd-backend/SKILL.md` resolve to files that exist in the same folder
- [ ] `tdd/` folder is deleted; no trace remains

---

## Phase 4: CLI — package scaffold + install

**User stories**: 14, 16, 18, 19, 20, 22, 23

### What to build

Create a Python package `ccskills` with a `pyproject.toml` defining the `ccskills` entry point. Implement `ccskills install`: discovers all skill directories in the installed package (any dir containing `SKILL.md`), copies all `.md` files from each skill dir to `<cwd>/.claude/skills/<skill-name>/`, creates directories as needed, overwrites existing files (idempotent). Prints confirmation listing which skills were installed. No external dependencies — stdlib only (`pathlib`, `shutil`, `argparse`).

### Acceptance criteria

- [ ] `pyproject.toml` defines `ccskills` entry point with no external deps
- [ ] `ccskills install` copies all `.md` files from each skill dir to `<cwd>/.claude/skills/<skill-name>/`
- [ ] Non-`.md` files are not copied
- [ ] Hidden files are not copied
- [ ] Re-running `ccskills install` overwrites existing files without error
- [ ] Output lists each skill installed
- [ ] Installable via `uv tool install git+<repo>`

---

## Phase 5: CLI — uninstall

**User stories**: 15, 17, 23

### What to build

Implement `ccskills uninstall`: removes `<cwd>/.claude/skills/<skill-name>/` for all known skills. No-ops gracefully if a skill directory was never installed (no error, no crash). Prints confirmation listing which skills were removed (or skipped).

### Acceptance criteria

- [ ] `ccskills uninstall` removes all skill subdirectories under `<cwd>/.claude/skills/`
- [ ] If a skill dir doesn't exist, command completes without error
- [ ] Output lists each skill removed or skipped
- [ ] Running uninstall on a clean directory exits cleanly

---

## Phase 6: CLI — tests

**User stories**: Testing Decisions (file installer + CLI integration)

### What to build

Write tests covering observable behaviour only — no mocking of stdlib. Use a temporary directory as `cwd` in all tests; never touch the real `.claude/`.

Two test areas:
- **File installer**: `install` creates correct directory structure and copies all `.md` files; non-`.md` files are not copied; `uninstall` removes correct directories; `uninstall` no-ops if directory doesn't exist.
- **CLI integration**: `ccskills install` end-to-end against a temp dir; `ccskills uninstall` end-to-end against a temp dir.

### Acceptance criteria

- [ ] Tests cover: install creates expected dirs and files
- [ ] Tests cover: install skips non-`.md` files
- [ ] Tests cover: uninstall removes installed dirs
- [ ] Tests cover: uninstall is safe when dirs don't exist
- [ ] CLI integration tests invoke `ccskills` as a subprocess against a temp dir
- [ ] No mocking of `shutil`, `pathlib`, or other stdlib
- [ ] All tests pass

---

## Phase 7: README

**User stories**: 21

### What to build

Update `README.md` with the exact install command (`uv tool install git+<repo>` / `uvx` usage) and usage instructions for `ccskills install` and `ccskills uninstall`.

### Acceptance criteria

- [ ] `README.md` contains exact `uv tool install` command
- [ ] `README.md` documents `ccskills install` and `ccskills uninstall` with example output
- [ ] No setup beyond the install command is required to get started
