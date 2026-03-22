# skills

Claude Code skills for software development workflows.

## Install

```sh
uvx --from git+https://github.com/wazzzy/cc skills install
```

## Usage

Run these commands from your project root.

### Install skills

Copies all skill files into `.claude/skills/` in the current directory:

```sh
uvx --from git+https://github.com/wazzzy/cc skills install
```

Example output:

```
  installed: interrogate
  installed: issues-from-prd
  installed: plan-from-prd
  installed: tdd-backend
  installed: tdd-frontend
  installed: write-prd

6 skill(s) installed to /your/project/.claude/skills
```

### List skills

Lists all available skills:

```sh
uvx --from git+https://github.com/wazzzy/cc skills list
```

Example output:

```
  interrogate
  issues-from-prd
  plan-from-prd
  tdd-backend
  tdd-frontend
  write-prd
```

### Uninstall skills

Removes all skill directories from `.claude/skills/`:

```sh
uvx --from git+https://github.com/wazzzy/cc skills uninstall
```

Example output:

```
  removed: interrogate
  removed: issues-from-prd
  removed: plan-from-prd
  removed: tdd-backend
  removed: tdd-frontend
  removed: write-prd

6 skill(s) removed, 0 skipped
```

Re-running `install` is safe — existing files are overwritten without error.

## Skills

| Skill | Description |
|---|---|
| `write-prd` | Create a PRD through user interview and codebase exploration |
| `plan-from-prd` | Turn a PRD into a multi-phase implementation plan |
| `issues-from-prd` | Break a PRD into independently-grabbable issues |
| `interrogate` | Stress-test a plan through relentless interviewing |
| `tdd-backend` | TDD for Python/Django with red-green-refactor |
| `tdd-frontend` | TDD for TypeScript/React/Next.js with RTL + Vitest |
