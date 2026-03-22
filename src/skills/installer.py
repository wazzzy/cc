"""File installer: copies skill .md files into <cwd>/.claude/skills/<skill-name>/."""

import shutil
from pathlib import Path


def _skills_root() -> Path:
    """Return the directory containing all skill folders (the package dir)."""
    return Path(__file__).parent


def discover_skills(skills_root: Path) -> list[Path]:
    """Return all skill dirs (top-level dirs containing SKILL.md)."""
    return sorted(
        d for d in skills_root.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )


def install(cwd: Path, names: list[str] | None = None) -> list[str]:
    """
    Copy skill .md files to <cwd>/.claude/skills/<skill-name>/.

    If names is given, only those skills are installed. Returns list of skill names installed.
    Raises ValueError for any name not found.
    """
    skills_root = _skills_root()
    skills = discover_skills(skills_root)

    if names is not None:
        known = {d.name for d in skills}
        unknown = [n for n in names if n not in known]
        if unknown:
            raise ValueError(f"unknown skill(s): {', '.join(unknown)}")
        skills = [d for d in skills if d.name in names]

    installed = []

    for skill_dir in skills:
        dest = cwd / ".claude" / "skills" / skill_dir.name
        dest.mkdir(parents=True, exist_ok=True)

        for src_file in skill_dir.iterdir():
            if src_file.is_file() and src_file.suffix == ".md" and not src_file.name.startswith("."):
                shutil.copy2(src_file, dest / src_file.name)

        installed.append(skill_dir.name)

    return installed


def uninstall(cwd: Path, names: list[str] | None = None) -> dict[str, str]:
    """
    Remove skill dirs from <cwd>/.claude/skills/.

    If names is given, only those skills are removed. Returns dict of skill_name -> "removed" | "skipped".
    Raises ValueError for any name not found.
    """
    skills_root = _skills_root()
    skills = discover_skills(skills_root)

    if names is not None:
        known = {d.name for d in skills}
        unknown = [n for n in names if n not in known]
        if unknown:
            raise ValueError(f"unknown skill(s): {', '.join(unknown)}")
        skills = [d for d in skills if d.name in names]

    results = {}

    for skill_dir in skills:
        dest = cwd / ".claude" / "skills" / skill_dir.name
        if dest.exists():
            shutil.rmtree(dest)
            results[skill_dir.name] = "removed"
        else:
            results[skill_dir.name] = "skipped"

    return results
