# ccskills — Documentation

> Inventory, gap analysis, and build plan for the personal Claude skills repo.

---

## 1. Decisions Log

| Decision | Value |
|---|---|
| Repo purpose | Personal skills library, installable on any remote via `uv`/`uvx` |
| Install target | `~/.claude/skills/` + `settings.json` registration |
| Tech stack (backend) | Python, Django |
| Tech stack (frontend) | React / Next.js (App Router), TypeScript, Tailwind CSS, Vitest, React Testing Library |
| Removed skill | `dev-browser` (out of scope) |

---

## 2. Current Skills Inventory

### `write-a-prd`
- **Files:** `SKILL.md`
- **Does:** Interviews user → explores codebase → generates PRD file
- **Status:** Content fine. Rename only.

### `prd-to-plan`
- **Files:** `SKILL.md`
- **Does:** Breaks PRD into multi-phase vertical-slice implementation plan → writes to `docs/plans/`
- **Status:** Content fine. Rename only.

### `prd-to-issues`
- **Files:** `SKILL.md`
- **Does:** Breaks PRD into independently-grabbable issue files in `docs/issues/`, HITL vs AFK classification
- **Status:** Content fine. Rename only.

### `grill-me`
- **Files:** `SKILL.md`
- **Does:** Relentlessly interviews user on a design/plan, walks decision tree, provides recommendations
- **Status:** Content fine. Rename only.

### `tdd`
- **Files:** `SKILL.md` *(carefully written — core philosophy off-limits)*, `backend-test.md`, `backend-mocking.md`, `frontend-test.md` *(minimal, needs expansion)*, `frontend-mocking.md`, `interface-design.md` *(frontend POV)*, `deep-modules.md` *(frontend POV)*, `refactoring.md` *(frontend POV)*
- **Does:** TDD workflow via red-green-refactor, vertical slices / tracer bullets
- **Status:** Split into two skills. See gap analysis below.

---

## 3. Naming Decisions

| Current | Final Name | Change Type |
|---|---|---|
| `write-a-prd` | `write-prd` | Rename |
| `prd-to-plan` | `plan-from-prd` | Rename |
| `prd-to-issues` | `issues-from-prd` | Rename |
| `grill-me` | `interrogate` | Rename |
| `tdd` | `tdd-backend` + `tdd-frontend` | Split into two skills |

---

## 4. Gap Analysis

### 4.1 `tdd` → `tdd-backend`

**Keep from `tdd/SKILL.md`:** entire philosophy section (core principle, good/bad tests, anti-pattern, workflow, checklist) — do not modify.

**Adapt:** references to file links (update to point to backend sub-docs).

**Move in:**
- `backend-test.md` — Django TestCase / APITestCase examples
- `backend-mocking.md` — patch where used, mock external APIs only

**Create (new):**
- `interface-design-backend.md` — Django/Python equivalents: views as interfaces, service layer design, accept deps / return results pattern
- `deep-modules-backend.md` — Django managers, service classes, utility modules hiding complexity
- `refactoring-backend.md` — Python-specific: duplication, long views, fat models, primitive obsession

---

### 4.2 `tdd` → `tdd-frontend`

**Keep from `tdd/SKILL.md`:** same core philosophy — do not modify.

**Move in (existing, written from frontend POV):**
- `frontend-mocking.md`
- `interface-design.md` → rename to `interface-design-frontend.md`
- `deep-modules.md` → rename to `deep-modules-frontend.md`
- `refactoring.md` → rename to `refactoring-frontend.md`

**Expand (currently minimal):**
- `frontend-test.md` — React Testing Library + Vitest, Next.js App Router patterns, component behavior testing (not implementation), async patterns

---

### 4.3 Skill description triggers

Every `SKILL.md` frontmatter `description` field needs a review. Claude uses this to decide when to invoke a skill — it must be precise and list natural trigger phrases.

Affected: all 5 skills after rename.

---

### 4.4 CLI distribution tool

Does not exist yet. Needs to be built.

**Spec:**
- Python package, installable via `uv tool install git+<repo>` or `uvx <package>`
- Single command (e.g. `ccskills install`)
- Copies all `SKILL.md` + supporting `.md` files to `~/.claude/skills/<skill-name>/`
- Registers skills in `~/.claude/settings.json` under the skills array
- Idempotent — safe to re-run, overwrites existing files, no duplicates in settings
- No dependencies beyond stdlib if possible (or minimal deps compatible with `uv`)

---

## 5. Proposed File Structure (Post-Refactor)

```
ccskills/
├── DOCS.md                         # this file
├── README.md                       # how to install via uv/uvx
├── pyproject.toml                  # Python package config
├── src/
│   └── ccskills/
│       ├── __init__.py
│       └── cli.py                  # install command
│
├── write-prd/
│   └── SKILL.md
│
├── plan-from-prd/
│   └── SKILL.md
│
├── issues-from-prd/
│   └── SKILL.md
│
├── interrogate/
│   └── SKILL.md
│
├── tdd-backend/
│   ├── SKILL.md                    # core TDD philosophy (adapted from tdd/SKILL.md)
│   ├── backend-test.md
│   ├── backend-mocking.md
│   ├── interface-design-backend.md # NEW
│   ├── deep-modules-backend.md     # NEW
│   └── refactoring-backend.md      # NEW
│
└── tdd-frontend/
    ├── SKILL.md                    # core TDD philosophy (adapted from tdd/SKILL.md)
    ├── frontend-test.md            # EXPAND: RTL + Vitest + Next.js App Router
    ├── frontend-mocking.md
    ├── interface-design-frontend.md # moved from tdd/interface-design.md
    ├── deep-modules-frontend.md     # moved from tdd/deep-modules.md
    └── refactoring-frontend.md      # moved from tdd/refactoring.md
```

---

## 6. Work Items (Ordered)

1. **Remove** `dev-browser/` directory
2. **Rename** skill folders: `write-a-prd` → `write-prd`, `prd-to-plan` → `plan-from-prd`, `prd-to-issues` → `issues-from-prd`, `grill-me` → `interrogate`
3. **Update** `name` + `description` fields in `SKILL.md` frontmatter for renamed skills
4. **Create** `tdd-backend/` — copy `tdd/SKILL.md` (preserve philosophy), move backend docs, create 3 new backend reference docs
5. **Create** `tdd-frontend/` — copy `tdd/SKILL.md` (preserve philosophy), move frontend docs (rename to `-frontend` suffix), expand `frontend-test.md`
6. **Delete** original `tdd/` folder
7. **Create** `pyproject.toml` + `src/ccskills/cli.py` — install command
8. **Create** `README.md` — uv/uvx install instructions
