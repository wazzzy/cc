# ccskills

Claude Code skills for software development workflows.

## Install

```sh
uv tool install git+https://github.com/wasimkarani/ccskills
```

Or run without installing:

```sh
uvx --from git+https://github.com/wasimkarani/ccskills ccskills install
```

## Usage

Run these commands from your project root.

### Install skills

Copies all skill files into `.claude/skills/` in the current directory:

```sh
ccskills install
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

### Uninstall skills

Removes all skill directories from `.claude/skills/`:

```sh
ccskills uninstall
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
