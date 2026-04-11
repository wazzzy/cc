"""File installer: copies skill .md files into user or project .claude/skills/."""

import shutil
from pathlib import Path


def _skills_root() -> Path:
    """Return the directory containing all skill folders (the package dir)."""
    return Path(__file__).parent


def parse_scope(skill_dir: Path) -> str:
    """Read SKILL.md frontmatter and return the scope value ('user' or 'project')."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return "project"
    text = skill_md.read_text()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return "project"
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("scope:"):
            return line.split(":", 1)[1].strip()
    return "project"


def _dest_path(cwd: Path, skill_name: str, scope: str, target: str = "claude") -> Path:
    """Return target directory for a skill based on its scope and target agent."""
    if target == "pi":
        if scope == "user":
            return Path.home() / ".pi" / "agent" / "skills" / skill_name
        return cwd / ".pi" / "skills" / skill_name
    if scope == "user":
        return Path.home() / ".claude" / "skills" / skill_name
    return cwd / ".claude" / "skills" / skill_name


def discover_skills(skills_root: Path) -> list[Path]:
    """Return all skill dirs (top-level dirs containing SKILL.md)."""
    return sorted(
        d for d in skills_root.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )


def list_skills() -> list[tuple[str, str]]:
    """Return (name, scope) for all available skills."""
    return [
        (d.name, parse_scope(d))
        for d in discover_skills(_skills_root())
    ]


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
