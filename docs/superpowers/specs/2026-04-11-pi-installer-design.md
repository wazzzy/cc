# Design: Pi Installer Support (`--pi` flag)

**Date:** 2026-04-11
**Status:** Approved

---

## Overview

Add `--pi` flag to the `skills install` and `skills uninstall` CLI commands so users can install skills into pi's skill directories (`.pi/skills/` and `~/.pi/agent/skills/`) using the same workflow as Claude Code.

---

## Architecture

Single-parameter extension to the existing installer. No new modules. No logic duplication.

The only thing that differs between Claude Code and pi installs is the **destination path**. Everything else — skill discovery, scope parsing, file filtering, idempotency — is identical.

---

## Components

### `src/skills/installer.py`

**`_dest_path(cwd, skill_name, scope, target="claude")`**

New `target` parameter routes to the correct base directory:

| target | scope | destination |
|--------|-------|-------------|
| `"claude"` | `"user"` | `~/.claude/skills/<name>/` |
| `"claude"` | `"project"` | `<cwd>/.claude/skills/<name>/` |
| `"pi"` | `"user"` | `~/.pi/agent/skills/<name>/` |
| `"pi"` | `"project"` | `<cwd>/.pi/skills/<name>/` |

**`install(cwd, names=None, target="claude")`**

`target` passed through to `_dest_path`. All other behaviour unchanged.

**`uninstall(cwd, names=None, target="claude")`**

Same — `target` passed through to `_dest_path`.

---

### `src/cc/skills_cli.py`

`--pi` flag added to `install` and `uninstall` subparsers:

```
skills install [--pi] [SKILL ...]
skills uninstall [--pi] [SKILL ...]
```

Handler sets `target = "pi" if args.pi else "claude"` and passes to installer.

`list` subcommand unchanged — shows source package skills regardless of target.

---

## Data Flow

```
skills install --pi tdd-backend
  → cmd_install: target="pi", names=["tdd-backend"]
  → install(cwd, ["tdd-backend"], target="pi")
  → _dest_path(cwd, "tdd-backend", "project", "pi")
  → cwd / ".pi" / "skills" / "tdd-backend"
  → copy .md files
```

---

## Testing

All new tests written **test-first** (red → green) following the tdd-backend skill.
Existing tests remain unchanged — no regressions.

### `tests/test_installer.py`

**`TestInstallPi`** — 8 unit behaviours:
1. User-scoped skill goes to `~/.pi/agent/skills/`
2. Project-scoped skill goes to `.pi/skills/`
3. Bare install (no names) only installs user-scoped skills
4. Copies `.md` files
5. Skips non-`.md` files
6. Skips hidden `.md` files
7. Idempotent (second install doesn't error)
8. Unknown skill name raises `ValueError`

**`TestUninstallPi`** — 4 unit behaviours:
9. Bare uninstall only removes user-scoped skills
10. Removes user skill from `~/.pi/agent/skills/`
11. Removes project skill from `.pi/skills/`
12. Returns `("skipped", scope)` when dir not present

### `tests/test_cli.py`

**`TestSkillsInstallPi`** — 4 integration behaviours:
13. `skills install --pi` exits 0
14. User skills land in `~/.pi/agent/skills/`
15. `skills install --pi tdd-backend` creates `.pi/skills/tdd-backend/`
16. `--pi` install does NOT touch `.claude/`

**`TestSkillsUninstallPi`** — 3 integration behaviours:
17. `skills uninstall --pi` exits 0
18. Removes skills from pi dir
19. Clean dir outputs `skipped`

---

## Error Handling

- Unknown skill names: `ValueError` raised by installer, caught by CLI → non-zero exit + message (same as existing)
- No new error cases introduced

---

## Constraints

- Default behaviour (`target="claude"`) is fully backward compatible
- No changes to `list`, `templates`, or any other command
- Existing `.claude/` tests remain untouched
