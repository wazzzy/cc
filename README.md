# cc

Claude Code skills and CLAUDE.md templates for software development workflows.

## Setup

Bootstrap Claude Code, configure PATH, and create a default `~/.claude/CLAUDE.md`:

```sh
curl -fsSL https://raw.githubusercontent.com/wazzzy/cc/main/setup.sh | bash
```

## Install

```sh
uvx --from git+https://github.com/wazzzy/cc cc skills install
```

## Usage

All commands use the unified `cc` CLI:

```
cc skills <install|uninstall|list> [--cwd DIR] [SKILL...]
cc template <init|list> [--cwd DIR] [args]
```

### skills

#### Install

Bare install copies user-scoped skills to `~/.claude/skills/`:

```sh
uvx --from git+https://github.com/wazzzy/cc cc skills install
```

Install a project-scoped skill to `.claude/skills/` in cwd:

```sh
uvx --from git+https://github.com/wazzzy/cc cc skills install tdd-backend
```

#### List

```sh
uvx --from git+https://github.com/wazzzy/cc cc skills list
```

```
  interrogate        (user)
  issues-from-prd    (user)
  plan-from-prd      (user)
  tdd-backend        (project)
  tdd-frontend       (project)
  write-prd          (user)
```

#### Uninstall

Bare uninstall removes user-scoped skills from `~/.claude/skills/`:

```sh
uvx --from git+https://github.com/wazzzy/cc cc skills uninstall
```

Named uninstall routes by scope:

```sh
uvx --from git+https://github.com/wazzzy/cc cc skills uninstall tdd-backend
```

### template

#### List

```sh
uvx --from git+https://github.com/wazzzy/cc cc template list
```

```
  django    (default: ./backend/)
```

#### Init

Copy the Django CLAUDE.md into `./backend/`:

```sh
uvx --from git+https://github.com/wazzzy/cc cc template init django
```

Custom target path:

```sh
uvx --from git+https://github.com/wazzzy/cc cc template init django --path ./my-app
```

Overwrite existing:

```sh
uvx --from git+https://github.com/wazzzy/cc cc template init django --force
```

## Skills

| Skill | Scope | Description |
|---|---|---|
| `interrogate` | user | Stress-test a plan through relentless interviewing |
| `write-prd` | user | Create a PRD through user interview and codebase exploration |
| `plan-from-prd` | user | Turn a PRD into a multi-phase implementation plan |
| `issues-from-prd` | user | Break a PRD into independently-grabbable issues |
| `tdd-backend` | project | TDD for Python/Django with red-green-refactor |
| `tdd-frontend` | project | TDD for TypeScript/React/Next.js with RTL + Vitest |

## Templates

| Template | Default path | Description |
|---|---|---|
| `django` | `./backend/` | CLAUDE.md for Python/Django projects |
