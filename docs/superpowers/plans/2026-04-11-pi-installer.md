# Pi Installer Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `--pi` flag to `skills install` and `skills uninstall` so skills are copied to `.pi/skills/` (project) or `~/.pi/agent/skills/` (user) instead of `.claude/`.

**Architecture:** Extend `_dest_path`, `install()`, and `uninstall()` in `src/skills/installer.py` with a `target` parameter (`"claude"` default, `"pi"` for pi). CLI gets a `--pi` flag that sets `target="pi"`. All existing behaviour and tests unchanged.

**Tech Stack:** Python 3.9+, pytest, unittest.mock, pathlib, subprocess (CLI tests)

---

## File Map

| File | Change |
|---|---|
| `src/skills/installer.py` | Add `target` param to `_dest_path`, `install`, `uninstall` |
| `src/cc/skills_cli.py` | Add `--pi` flag to `install` and `uninstall` subcommands |
| `tests/test_installer.py` | Add `TestInstallPi` and `TestUninstallPi` classes |
| `tests/test_cli.py` | Add `TestSkillsInstallPi` and `TestSkillsUninstallPi` classes |

---

## Task 1 — Tracer Bullet: user skill installs to `~/.pi/agent/skills/`

**Files:**
- Modify: `tests/test_installer.py`
- Modify: `src/skills/installer.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_installer.py` after the existing `TestInstall` class:

```python
class TestInstallPi:
    def test_user_skill_goes_to_pi_agent_dir(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path, target="pi")
        assert (fake_home / ".pi" / "agent" / "skills" / "skill-user-a" / "SKILL.md").exists()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /path/to/cc
uv run pytest tests/test_installer.py::TestInstallPi::test_user_skill_goes_to_pi_agent_dir -v
```

Expected: `FAILED` — `TypeError: install() got an unexpected keyword argument 'target'`

- [ ] **Step 3: Implement minimal code**

In `src/skills/installer.py`, replace `_dest_path` and `install` signatures:

```python
def _dest_path(cwd: Path, skill_name: str, scope: str, target: str = "claude") -> Path:
    """Return target directory for a skill based on its scope and target agent."""
    if target == "pi":
        if scope == "user":
            return Path.home() / ".pi" / "agent" / "skills" / skill_name
        return cwd / ".pi" / "skills" / skill_name
    if scope == "user":
        return Path.home() / ".claude" / "skills" / skill_name
    return cwd / ".claude" / "skills" / skill_name


def install(cwd: Path, names: list[str] | None = None, target: str = "claude") -> list[tuple[str, str, Path]]:
    """
    Copy skill .md files to user or project skills directory.

    Bare install (names=None) only installs scope:user skills.
    Named install routes each skill by its scope.
    target="claude" installs to .claude/skills/ (default).
    target="pi" installs to .pi/skills/ or ~/.pi/agent/skills/.
    Returns list of (name, scope, dest_path).
    Raises ValueError for unknown names.
    """
    skills_root = _skills_root()
    skills = discover_skills(skills_root)

    if names is not None:
        known = {d.name for d in skills}
        unknown = [n for n in names if n not in known]
        if unknown:
            raise ValueError(f"unknown skill(s): {', '.join(unknown)}")
        skills = [d for d in skills if d.name in names]
    else:
        skills = [d for d in skills if parse_scope(d) == "user"]

    installed = []

    for skill_dir in skills:
        scope = parse_scope(skill_dir)
        dest = _dest_path(cwd, skill_dir.name, scope, target)
        dest.mkdir(parents=True, exist_ok=True)

        for src_file in skill_dir.iterdir():
            if src_file.is_file() and src_file.suffix == ".md" and not src_file.name.startswith("."):
                shutil.copy2(src_file, dest / src_file.name)

        installed.append((skill_dir.name, scope, dest))

    return installed
```

- [ ] **Step 4: Run test to verify it passes**

```bash
uv run pytest tests/test_installer.py::TestInstallPi::test_user_skill_goes_to_pi_agent_dir -v
```

Expected: `PASSED`

- [ ] **Step 5: Verify no regressions**

```bash
uv run pytest tests/test_installer.py -v
```

Expected: all existing tests still `PASSED`

- [ ] **Step 6: Commit**

```bash
git add src/skills/installer.py tests/test_installer.py
git commit -m "feat: tracer bullet — pi user skill installs to ~/.pi/agent/skills/"
```

---

## Task 2 — Project skill installs to `.pi/skills/`

**Files:**
- Modify: `tests/test_installer.py`
- No new code needed (already handled by `_dest_path`)

- [ ] **Step 1: Write the failing test**

Add to `TestInstallPi` in `tests/test_installer.py`:

```python
    def test_project_skill_goes_to_pi_skills_dir(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(cwd, ["skill-proj"], target="pi")
        assert (cwd / ".pi" / "skills" / "skill-proj" / "SKILL.md").exists()
```

- [ ] **Step 2: Run test to verify it fails or passes**

```bash
uv run pytest tests/test_installer.py::TestInstallPi::test_project_skill_goes_to_pi_skills_dir -v
```

Expected: `PASSED` — `_dest_path` already handles the project pi case from Task 1.
If `FAILED`, the project branch in `_dest_path` is missing — verify the `return cwd / ".pi" / "skills" / skill_name` line is present.

- [ ] **Step 3: Commit**

```bash
git add tests/test_installer.py
git commit -m "test: pi project skill goes to .pi/skills/"
```

---

## Task 3 — Bare pi install skips project-scoped skills

**Files:**
- Modify: `tests/test_installer.py`

- [ ] **Step 1: Write the failing test**

Add to `TestInstallPi`:

```python
    def test_bare_install_only_user_scope(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            result = install(cwd, target="pi")
        names = [n for n, _, _ in result]
        assert "skill-user-a" in names
        assert "skill-user-b" in names
        assert "skill-proj" not in names
```

- [ ] **Step 2: Run test**

```bash
uv run pytest tests/test_installer.py::TestInstallPi::test_bare_install_only_user_scope -v
```

Expected: `PASSED` — scope filtering logic is shared, no new code needed.

- [ ] **Step 3: Commit**

```bash
git add tests/test_installer.py
git commit -m "test: bare pi install only installs user-scoped skills"
```

---

## Task 4 — Pi install copies `.md` files and skips non-md and hidden files

**Files:**
- Modify: `tests/test_installer.py`

- [ ] **Step 1: Write the failing tests**

Add to `TestInstallPi`:

```python
    def test_copies_md_files(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path, target="pi")
        assert (fake_home / ".pi" / "agent" / "skills" / "skill-user-a" / "guide.md").exists()

    def test_skips_non_md_files(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path, target="pi")
        assert not (fake_home / ".pi" / "agent" / "skills" / "skill-user-a" / "not-markdown.txt").exists()

    def test_skips_hidden_files(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path, target="pi")
        assert not (fake_home / ".pi" / "agent" / "skills" / "skill-user-a" / ".hidden.md").exists()
```

- [ ] **Step 2: Run tests**

```bash
uv run pytest tests/test_installer.py::TestInstallPi::test_copies_md_files tests/test_installer.py::TestInstallPi::test_skips_non_md_files tests/test_installer.py::TestInstallPi::test_skips_hidden_files -v
```

Expected: all `PASSED` — file filtering is shared logic, no new code needed.

- [ ] **Step 3: Commit**

```bash
git add tests/test_installer.py
git commit -m "test: pi install copies md files, skips non-md and hidden"
```

---

## Task 5 — Pi install is idempotent and rejects unknown skills

**Files:**
- Modify: `tests/test_installer.py`

- [ ] **Step 1: Write the failing tests**

Add to `TestInstallPi`:

```python
    def test_idempotent(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path, target="pi")
            install(tmp_path, target="pi")
        assert (fake_home / ".pi" / "agent" / "skills" / "skill-user-a" / "SKILL.md").exists()

    def test_install_unknown_raises(self, fake_skills_root: Path, tmp_path: Path):
        with _patch_root(fake_skills_root):
            with pytest.raises(ValueError, match="unknown skill"):
                install(tmp_path, ["nope"], target="pi")
```

- [ ] **Step 2: Run tests**

```bash
uv run pytest tests/test_installer.py::TestInstallPi::test_idempotent tests/test_installer.py::TestInstallPi::test_install_unknown_raises -v
```

Expected: both `PASSED` — idempotency and unknown-skill error are shared logic.

- [ ] **Step 3: Commit**

```bash
git add tests/test_installer.py
git commit -m "test: pi install is idempotent and rejects unknown skills"
```

---

## Task 6 — Tracer Bullet: `uninstall()` accepts `target` param

**Files:**
- Modify: `tests/test_installer.py`
- Modify: `src/skills/installer.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_installer.py` after `TestInstallPi`:

```python
class TestUninstallPi:
    def test_bare_uninstall_only_user_scope(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(cwd, target="pi")
            install(cwd, ["skill-proj"], target="pi")
            results = uninstall(cwd, target="pi")
        assert "skill-user-a" in results
        assert "skill-user-b" in results
        assert "skill-proj" not in results
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run pytest tests/test_installer.py::TestUninstallPi::test_bare_uninstall_only_user_scope -v
```

Expected: `FAILED` — `TypeError: uninstall() got an unexpected keyword argument 'target'`

- [ ] **Step 3: Implement minimal code**

In `src/skills/installer.py`, update `uninstall` signature and `_dest_path` call:

```python
def uninstall(cwd: Path, names: list[str] | None = None, target: str = "claude") -> dict[str, tuple[str, str]]:
    """
    Remove skill dirs from user or project skills directory.

    Bare uninstall (names=None) only removes scope:user skills.
    Named uninstall routes each skill by its scope.
    target="claude" removes from .claude/skills/ (default).
    target="pi" removes from .pi/skills/ or ~/.pi/agent/skills/.
    Returns dict of skill_name -> (status, scope).
    Raises ValueError for unknown names.
    """
    skills_root = _skills_root()
    skills = discover_skills(skills_root)

    if names is not None:
        known = {d.name for d in skills}
        unknown = [n for n in names if n not in known]
        if unknown:
            raise ValueError(f"unknown skill(s): {', '.join(unknown)}")
        skills = [d for d in skills if d.name in names]
    else:
        skills = [d for d in skills if parse_scope(d) == "user"]

    results = {}

    for skill_dir in skills:
        scope = parse_scope(skill_dir)
        dest = _dest_path(cwd, skill_dir.name, scope, target)
        if dest.exists():
            shutil.rmtree(dest)
            results[skill_dir.name] = ("removed", scope)
        else:
            results[skill_dir.name] = ("skipped", scope)

    return results
```

- [ ] **Step 4: Run test to verify it passes**

```bash
uv run pytest tests/test_installer.py::TestUninstallPi::test_bare_uninstall_only_user_scope -v
```

Expected: `PASSED`

- [ ] **Step 5: Verify no regressions**

```bash
uv run pytest tests/test_installer.py -v
```

Expected: all tests `PASSED`

- [ ] **Step 6: Commit**

```bash
git add src/skills/installer.py tests/test_installer.py
git commit -m "feat: uninstall() accepts target param for pi support"
```

---

## Task 7 — Remaining uninstall pi behaviours

**Files:**
- Modify: `tests/test_installer.py`

- [ ] **Step 1: Write the failing tests**

Add to `TestUninstallPi`:

```python
    def test_removes_user_skill_from_pi_agent_dir(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path, target="pi")
            uninstall(tmp_path, target="pi")
        assert not (fake_home / ".pi" / "agent" / "skills" / "skill-user-a").exists()

    def test_removes_project_skill_from_pi_skills_dir(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(cwd, ["skill-proj"], target="pi")
            results = uninstall(cwd, ["skill-proj"], target="pi")
        assert results["skill-proj"] == ("removed", "project")
        assert not (cwd / ".pi" / "skills" / "skill-proj").exists()

    def test_noop_when_not_installed(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            results = uninstall(tmp_path, target="pi")
        assert results["skill-user-a"] == ("skipped", "user")
```

- [ ] **Step 2: Run tests**

```bash
uv run pytest tests/test_installer.py::TestUninstallPi -v
```

Expected: all `PASSED` — removal and noop logic is shared.

- [ ] **Step 3: Commit**

```bash
git add tests/test_installer.py
git commit -m "test: pi uninstall removes skills and skips missing"
```

---

## Task 8 — Tracer Bullet: CLI `skills install --pi` exits 0

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `src/cc/skills_cli.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_cli.py` after the existing `TestSkillsUninstall` class:

```python
class TestSkillsInstallPi:
    def test_pi_install_exits_zero(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_skills("install", "--pi", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run pytest tests/test_cli.py::TestSkillsInstallPi::test_pi_install_exits_zero -v
```

Expected: `FAILED` — `error: unrecognized arguments: --pi`

- [ ] **Step 3: Implement minimal code**

In `src/cc/skills_cli.py`, add `--pi` flag to `install_p` and update `cmd_install`:

```python
def cmd_install(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    names = args.skills or None
    target = "pi" if args.pi else "claude"
    if args.cwd and names is None:
        print("warning: --cwd has no effect on user-level skills")
    try:
        results = install(cwd, names, target=target)
    except ValueError as e:
        print(f"error: {e}")
        raise SystemExit(1)
    for name, scope, dest in results:
        print(f"  installed: {name} ({scope}) -> {dest}")
    print(f"\n{len(results)} skill(s) installed")
```

And in `main()`, add the flag to `install_p`:

```python
install_p = subparsers.add_parser("install", help="Install skills (user-scoped by default)")
install_p.add_argument("skills", nargs="*", metavar="SKILL")
install_p.add_argument("--pi", action="store_true", help="Install into pi skills directory")
install_p.set_defaults(func=cmd_install)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
uv run pytest tests/test_cli.py::TestSkillsInstallPi::test_pi_install_exits_zero -v
```

Expected: `PASSED`

- [ ] **Step 5: Verify no regressions**

```bash
uv run pytest tests/test_cli.py -v
```

Expected: all existing tests still `PASSED`

- [ ] **Step 6: Commit**

```bash
git add src/cc/skills_cli.py tests/test_cli.py
git commit -m "feat: add --pi flag to skills install CLI"
```

---

## Task 9 — Remaining CLI install pi behaviours

**Files:**
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write the failing tests**

Add to `TestSkillsInstallPi`:

```python
    def test_pi_install_creates_user_skills_in_pi_dir(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", "--pi", cwd_arg=tmp_path, home=home)
        skills_dir = home / ".pi" / "agent" / "skills"
        assert skills_dir.is_dir()
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        assert len(skill_dirs) > 0
        for skill_dir in skill_dirs:
            assert (skill_dir / "SKILL.md").exists()

    def test_pi_install_project_skill(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_skills("install", "--pi", "tdd-backend", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0
        assert (tmp_path / ".pi" / "skills" / "tdd-backend" / "SKILL.md").exists()
        assert not (home / ".pi" / "agent" / "skills" / "tdd-backend").exists()

    def test_pi_install_does_not_touch_claude_dir(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", "--pi", cwd_arg=tmp_path, home=home)
        assert not (home / ".claude" / "skills").exists()
```

- [ ] **Step 2: Run tests**

```bash
uv run pytest tests/test_cli.py::TestSkillsInstallPi -v
```

Expected: all `PASSED`

- [ ] **Step 3: Commit**

```bash
git add tests/test_cli.py
git commit -m "test: CLI --pi install puts skills in pi dirs, not claude dirs"
```

---

## Task 10 — Tracer Bullet: CLI `skills uninstall --pi` exits 0

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `src/cc/skills_cli.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_cli.py` after `TestSkillsInstallPi`:

```python
class TestSkillsUninstallPi:
    def test_pi_uninstall_exits_zero(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", "--pi", cwd_arg=tmp_path, home=home)
        result = run_skills("uninstall", "--pi", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
uv run pytest tests/test_cli.py::TestSkillsUninstallPi::test_pi_uninstall_exits_zero -v
```

Expected: `FAILED` — `error: unrecognized arguments: --pi`

- [ ] **Step 3: Implement minimal code**

In `src/cc/skills_cli.py`, add `--pi` flag to `uninstall_p` and update `cmd_uninstall`:

```python
def cmd_uninstall(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    names = args.skills or None
    target = "pi" if args.pi else "claude"
    if args.cwd and names is None:
        print("warning: --cwd has no effect on user-level skills")
    try:
        results = uninstall(cwd, names, target=target)
    except ValueError as e:
        print(f"error: {e}")
        raise SystemExit(1)
    for name, (status, scope) in results.items():
        print(f"  {status}: {name} ({scope})")
    removed = sum(1 for s, _ in results.values() if s == "removed")
    skipped = sum(1 for s, _ in results.values() if s == "skipped")
    print(f"\n{removed} removed, {skipped} skipped")
```

And in `main()`, add the flag to `uninstall_p`:

```python
uninstall_p = subparsers.add_parser("uninstall", help="Uninstall skills")
uninstall_p.add_argument("skills", nargs="*", metavar="SKILL")
uninstall_p.add_argument("--pi", action="store_true", help="Uninstall from pi skills directory")
uninstall_p.set_defaults(func=cmd_uninstall)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
uv run pytest tests/test_cli.py::TestSkillsUninstallPi::test_pi_uninstall_exits_zero -v
```

Expected: `PASSED`

- [ ] **Step 5: Verify no regressions**

```bash
uv run pytest tests/test_cli.py -v
```

Expected: all tests `PASSED`

- [ ] **Step 6: Commit**

```bash
git add src/cc/skills_cli.py tests/test_cli.py
git commit -m "feat: add --pi flag to skills uninstall CLI"
```

---

## Task 11 — Remaining CLI uninstall pi behaviours

**Files:**
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write the failing tests**

Add to `TestSkillsUninstallPi`:

```python
    def test_pi_uninstall_removes_skills(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", "--pi", cwd_arg=tmp_path, home=home)
        run_skills("uninstall", "--pi", cwd_arg=tmp_path, home=home)
        skills_dir = home / ".pi" / "agent" / "skills"
        remaining = [d for d in skills_dir.iterdir() if d.is_dir()] if skills_dir.exists() else []
        assert remaining == []

    def test_pi_uninstall_clean_dir_has_skipped(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_skills("uninstall", "--pi", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0
        assert "skipped" in result.stdout
```

- [ ] **Step 2: Run tests**

```bash
uv run pytest tests/test_cli.py::TestSkillsUninstallPi -v
```

Expected: both `PASSED`

- [ ] **Step 3: Commit**

```bash
git add tests/test_cli.py
git commit -m "test: CLI --pi uninstall removes skills and outputs skipped"
```

---

## Task 12 — Full suite verification

- [ ] **Step 1: Run full test suite**

```bash
uv run pytest -v --tb=short
```

Expected: all tests `PASSED`, no warnings.

- [ ] **Step 2: Commit if clean**

```bash
git add -A
git commit -m "feat: pi installer support complete — --pi flag for install/uninstall"
```
