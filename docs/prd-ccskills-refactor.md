# PRD: ccskills Refactor + CLI Distribution Tool

## Problem Statement

The ccskills repo is a personal library of Claude Code skills, but it has two problems:

1. **Skills are poorly organised.** The `tdd` skill mixes frontend and backend guidance into one skill, creating noise for each context. Folder names are verbose or inconsistent. Frontmatter descriptions are imprecise, causing Claude to invoke skills at wrong times or miss them when relevant.

2. **Installation is manual.** There is no automated way to install skills into a project. Currently, files must be hand-copied to `.claude/skills/`. This is error-prone and slow.

---

## Solution

Reorganise the skill library (renames, splits, new content, frontmatter fixes) and build a Python CLI tool (`ccskills`) installable via `uv`/`uvx` that automates installing and uninstalling skills in any project.

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
13. As a developer, I want `frontend-test.md` to include RTL + Vitest examples with Next.js App Router patterns and async testing, so that the frontend TDD skill has concrete test examples.

### CLI Tool

14. As a developer, I want to run `ccskills install` in any project directory, so that all skills are automatically copied to `.claude/skills/`.
15. As a developer, I want to run `ccskills uninstall` in any project directory, so that all skills are removed from `.claude/skills/`.
16. As a developer, I want `ccskills install` to be idempotent, so that re-running it overwrites existing files.
17. As a developer, I want `ccskills uninstall` to be safe to run even if skills were never installed, so that it exits cleanly without errors.
18. As a developer, I want the CLI to install only `SKILL.md` and supporting `.md` files (no hidden files, no non-markdown files), so that the install is clean and minimal.
19. As a developer, I want each skill installed to its own subdirectory (e.g. `.claude/skills/tdd-backend/`), so that skills are isolated and easy to inspect.
20. As a developer, I want the tool installable via `uv tool install git+<repo>` or runnable via `uvx`, so that I can install it globally in seconds on any machine.
21. As a developer, I want a `README.md` with the exact install command and usage, so that I can get set up immediately.
22. As a developer, I want the CLI to have no external dependencies beyond Python stdlib (or minimal compatible deps), so that `uv`/`uvx` installs quickly.
23. As a developer, I want confirmation output after `install` and `uninstall` listing which skills were affected, so that I know the operation succeeded.

---

## Implementation Decisions

### Skill Library Reorganisation

- **Rename folders**: `write-a-prd` → `write-prd`, `prd-to-plan` → `plan-from-prd`, `prd-to-issues` → `issues-from-prd`, `grill-me` → `interrogate`. Update `name` field in each `SKILL.md` frontmatter to match.
- **Split `tdd/` into two skills**:
  - `tdd-backend/`: copy `tdd/SKILL.md` philosophy verbatim; include `backend-test.md`, `backend-mocking.md`; create `interface-design-backend.md` (backend section extracted from current `interface-design.md`), `deep-modules-backend.md` (new, Django-specific), `refactoring-backend.md` (new, Python-specific). Update internal doc links in `SKILL.md` to point to backend files.
  - `tdd-frontend/`: copy `tdd/SKILL.md` philosophy verbatim; include `frontend-test.md`, `frontend-mocking.md`; create `interface-design-frontend.md` (frontend section extracted from current `interface-design.md`), `deep-modules-frontend.md` (renamed from `deep-modules.md`), `refactoring-frontend.md` (renamed from `refactoring.md`). Update internal doc links in `SKILL.md` to point to frontend files.
- **Delete** original `tdd/` folder after split is complete.
- **Frontmatter `description` updates**: review and tighten trigger phrases for all 6 final skills (`write-prd`, `plan-from-prd`, `issues-from-prd`, `interrogate`, `tdd-backend`, `tdd-frontend`).

### CLI Tool

- **Package**: Python package `ccskills`, defined in `pyproject.toml`. Entry point: `ccskills` command.
- **Commands**: `ccskills install` and `ccskills uninstall`.
- **Install behaviour**:
  - Discovers all skill directories in the package (any top-level dir containing `SKILL.md`).
  - Copies all `.md` files from each skill dir to `<cwd>/.claude/skills/<skill-name>/`.
  - Idempotent: overwrites files.
- **Uninstall behaviour**:
  - Removes `<cwd>/.claude/skills/<skill-name>/` directories for all known skills.
  - No-ops gracefully if skills were never installed.
- **Skill discovery module**: encapsulates finding skill directories from the installed package location. Returns a list of `(skill_name, source_dir)` pairs.
- **File copy module**: encapsulates copying `.md` files from source to destination, creating directories as needed.
- **No external dependencies** beyond Python stdlib (`json`, `shutil`, `pathlib`, `argparse`).

---

## Testing Decisions

Good tests verify observable behaviour through public interfaces — they assert what the system does (files created), not how it does it (internal function calls, private state).

### Modules to test

- **File installer**: test that `install` creates correct directory structure and copies all `.md` files; test that non-`.md` files are not copied; test that `uninstall` removes the correct directories; test that `uninstall` no-ops if directory doesn't exist.
- **CLI integration**: test `ccskills install` end-to-end against a temp directory; test `ccskills uninstall` end-to-end against a temp directory.

### What makes a good test here

- Use a temporary directory as `cwd` — never touch the real `.claude/`.
- No mocking of stdlib (`shutil`, `json`, `pathlib`) — these are fast enough to run for real.

---

## Out of Scope

- Global install (`~/.claude/skills/`) — local project install only.
- `ccskills list` or other informational subcommands.
- Skill version management or upgrade diffing.
- Publishing to PyPI (only `uv tool install git+<repo>` / `uvx` via git).
- Windows path support (Unix paths only for now).
- Any changes to the core TDD philosophy text in `SKILL.md`.

---

## Further Notes

- The `interface-design.md` file currently contains both frontend and backend sections. The split must preserve both sections — nothing is lost, just separated into the right skill.
- `tdd/SKILL.md` currently has broken internal links (`tests.md`, `mocking.md`) that must be fixed in both `tdd-backend` and `tdd-frontend` copies.
