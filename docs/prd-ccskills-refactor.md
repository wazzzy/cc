# PRD: cc — Personal Dev Toolkit

## Problem Statement

The `cc` repo is a personal library of Claude Code skills and project templates, but it had two problems:

1. **Skills were poorly organised.** The `tdd` skill mixed frontend and backend guidance into one skill, creating noise for each context. Folder names were verbose or inconsistent. Frontmatter descriptions were imprecise, causing Claude to invoke skills at wrong times or miss them when relevant.

2. **Installation was manual.** There was no automated way to install skills or templates into a project. Files had to be hand-copied. This was error-prone and slow.

---

## Solution

Reorganise the skill library (renames, splits, new content, frontmatter fixes) and build two Python CLI tools (`skills` and `templates`) installable via `uv`/`uvx` that automate installing and uninstalling skills and templates in any project.

The repo (`cc`) is a personal dev toolkit. `skills` and `templates` are its two bootstrapping concerns. Growth path is content-only: new skill dirs and new template dirs are auto-discovered with no code changes required.

---

## User Stories

### Skill Library

1. As a developer using Claude for frontend work, I want a dedicated `tdd-frontend` skill with React Testing Library, Vitest, and Next.js App Router patterns, so that I get frontend-specific TDD guidance without backend noise.
2. As a developer using Claude for backend work, I want a dedicated `tdd-backend` skill with Django/Python-specific examples, so that I get backend-specific TDD guidance without frontend noise.
3. As a developer, I want each TDD skill to reference only the doc files relevant to its context, so that internal links are not broken and navigation is clear.
4. As a developer, I want `interface-design-frontend.md` to contain only frontend (TypeScript/React) patterns, so that the backend section does not appear in frontend TDD sessions.
5. As a developer, I want `interface-design-backend.md` to contain only Django/Python patterns, so that the frontend section does not appear in backend TDD sessions.
6. As a developer, I want `deep-modules-backend.md` with Django-specific examples (managers, service classes, utility modules), so that I can apply deep module design in Python projects.
7. As a developer, I want `refactoring-backend.md` with Python-specific refactoring candidates (long views, fat models, primitive obsession), so that I have concrete backend refactoring guidance.
8. As a developer, I want the `tdd` skill core philosophy (vertical slices, tracer bullets, red-green-refactor, checklist) preserved verbatim in both `tdd-backend` and `tdd-frontend`, so that the foundational approach is not diluted.
9. As a developer, I want the original `tdd/` folder removed after the split, so that the deprecated skill is not accidentally invoked.
10. As a developer, I want skill folder names to be short and predictable (`write-prd`, `plan-from-prd`, `issues-from-prd`, `interrogate`), so that I can reference them quickly.
11. As a developer, I want each skill's frontmatter `description` field to list precise natural trigger phrases, so that Claude invokes the right skill at the right time.
12. As a developer, I want `frontend-test.md` to include RTL + Vitest examples with Next.js App Router patterns and async testing, so that the frontend TDD skill has concrete test examples.

### skills CLI

13. As a developer, I want to run `skills install` in any project directory, so that all user-scoped skills are automatically copied to `~/.claude/skills/`.
14. As a developer, I want to run `skills install <name>` to install a named skill routed by its scope — user-scoped skills go to `~/.claude/skills/`, project-scoped to `.claude/skills/` in cwd.
15. As a developer, I want to run `skills uninstall` to remove all user-scoped skills from `~/.claude/skills/`.
16. As a developer, I want to run `skills uninstall <name>` to remove a named skill from its scoped location.
17. As a developer, I want `skills install` to be idempotent, so that re-running it overwrites existing files without error.
18. As a developer, I want `skills uninstall` to be safe to run even if skills were never installed, so that it exits cleanly.
19. As a developer, I want the CLI to install only `SKILL.md` and supporting `.md` files (no hidden files, no non-markdown files), so that the install is clean and minimal.
20. As a developer, I want each skill installed to its own subdirectory (e.g. `.claude/skills/tdd-backend/`), so that skills are isolated and easy to inspect.
21. As a developer, I want to run `skills list` to see all available skills and their scopes.
22. As a developer, I want confirmation output after `install` and `uninstall` listing which skills were affected, so that I know the operation succeeded.

### templates CLI

23. As a developer, I want to run `templates <name>` to copy a `CLAUDE.md` template into the default path in my project (e.g. `./backend/`), so that I get a pre-configured Claude context file without manual copying.
24. As a developer, I want to run `templates <name> --path <dir>` to install a template into a custom directory.
25. As a developer, I want `templates <name>` to skip the copy if `CLAUDE.md` already exists, so that I don't accidentally overwrite a customised file.
26. As a developer, I want `templates <name> --force` to overwrite an existing `CLAUDE.md`, so that I can update to the latest version when I choose.
27. As a developer, I want to run `templates list` to see all available templates and their default paths.

### Distribution

28. As a developer, I want both tools installable via `uvx --from git+<repo>`, so that I can use them on any machine with no global install required.
29. As a developer, I want a `README.md` with the exact install commands and usage, so that I can get set up immediately.
30. As a developer, I want both CLIs to have no external dependencies beyond Python stdlib, so that `uvx` runs quickly.

---

## Implementation Decisions

### Skill Library Reorganisation

- **Renamed folders**: `write-a-prd` → `write-prd`, `prd-to-plan` → `plan-from-prd`, `prd-to-issues` → `issues-from-prd`, `grill-me` → `interrogate`. `name` field in each `SKILL.md` matches folder name.
- **Split `tdd/` into two skills**:
  - `tdd-backend/` (scope: project): philosophy verbatim from `tdd/SKILL.md`; `backend-test.md`, `backend-mocking.md`, `interface-design-backend.md`, `deep-modules-backend.md`, `refactoring-backend.md`.
  - `tdd-frontend/` (scope: project): philosophy verbatim from `tdd/SKILL.md`; `frontend-test.md`, `frontend-mocking.md`, `interface-design-frontend.md`, `deep-modules-frontend.md`, `refactoring-frontend.md`.
- **Deleted** original `tdd/` folder.
- **Frontmatter `description`**: tightened trigger phrases for all 6 final skills.

### Skill Scopes

Skills have a `scope` field in their `SKILL.md` frontmatter (`user` or `project`):

- **`scope: user`** — installed to `~/.claude/skills/<name>/`. These are workflow skills useful in every project (`interrogate`, `write-prd`, `plan-from-prd`, `issues-from-prd`). Bare `skills install` (no arguments) installs all user-scoped skills.
- **`scope: project`** — installed to `<cwd>/.claude/skills/<name>/`. These are technical skills tied to a specific stack (`tdd-backend`, `tdd-frontend`). Must be installed by name: `skills install tdd-backend`.

### skills CLI

- **Package**: `cc` (`pyproject.toml`). Entry point: `skills`.
- **Commands**: `skills install [SKILL...]`, `skills uninstall [SKILL...]`, `skills list`.
- **Install (bare)**: discovers all skill directories in package (any top-level dir containing `SKILL.md`), installs only user-scoped skills to `~/.claude/skills/<name>/`.
- **Install (named)**: installs named skills routed by their scope.
- **Uninstall (bare)**: removes user-scoped skill dirs from `~/.claude/skills/`.
- **Uninstall (named)**: removes named skill dirs from their scoped location.
- **Idempotent**: overwrites files on re-install; no-ops gracefully on uninstall if dir doesn't exist.
- **File filter**: copies only `.md` files; skips hidden files and non-markdown files.
- **No external dependencies** — stdlib only (`pathlib`, `shutil`, `argparse`).

### templates CLI

- **Entry point**: `templates`.
- **Commands**: `templates <name> [--path DIR] [--force]`, `templates list`.
- **Template discovery**: any top-level dir in `src/templates/` containing both `TEMPLATE.md` (frontmatter: `name`, `default_path`, `description`) and `CLAUDE.md`.
- **Install behaviour**: copies `CLAUDE.md` from the template dir to `<cwd>/<default_path>/CLAUDE.md` (or `--path` override). Skips if destination exists unless `--force`.
- **Status output**: reports `created`, `skipped`, or `overwritten`.
- **No external dependencies** — stdlib only.

### Current templates

| Name | Default path | Description |
|---|---|---|
| `django` | `backend/` | Python/Django project |
| `django-helix` | `backend/` | Python/Django + Helix project |

---

## Testing Decisions

Good tests verify observable behaviour through public interfaces — they assert what the system does (files created, files removed), not how it does it.

### Modules tested

- **`skills.installer`**: install creates correct dirs and copies all `.md` files; non-`.md` and hidden files skipped; bare install only installs user-scoped; named install routes by scope; uninstall removes correct dirs; uninstall no-ops if dir doesn't exist; unknown name raises `ValueError`.
- **`templates.installer`**: init creates CLAUDE.md at default path; init skips if exists; init overwrites with force; unknown template raises `ValueError`.
- **CLI integration (`cc.skills_cli`)**: `skills install/uninstall/list` invoked as subprocess against a temp dir; project-scoped skills go to cwd; user-scoped skills go to home.
- **CLI integration (`cc.templates_cli`)**: `templates django` creates file; skips existing; `--force` overwrites; `--path` customises target; unknown template exits non-zero.

### Test constraints

- Temporary directory as `cwd` in all tests — never touch the real `.claude/`.
- No mocking of stdlib (`shutil`, `pathlib`).

---

## Out of Scope

- Skill version management or upgrade diffing.
- Publishing to PyPI (only `uvx --from git+<repo>` via git).
- Windows path support (Unix paths only).
- Any changes to the core TDD philosophy text.
- Global `cc` unified entry point (skills and templates remain separate commands).
