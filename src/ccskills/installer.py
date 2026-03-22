"""File installer: copies skill .md files into <cwd>/.claude/skills/<skill-name>/."""

import shutil
from pathlib import Path


def _skills_root() -> Path:
    """Return the directory containing all skill folders (the package root)."""
    return Path(__file__).parent.parent.parent


def discover_skills(skills_root: Path) -> list[Path]:
    """Return all skill dirs (top-level dirs containing SKILL.md)."""
    return sorted(
        d for d in skills_root.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )


def install(cwd: Path) -> list[str]:
    """
    Copy all skill .md files to <cwd>/.claude/skills/<skill-name>/.

    Returns list of skill names installed.
    """
    skills_root = _skills_root()
    skills = discover_skills(skills_root)
    installed = []

    for skill_dir in skills:
        dest = cwd / ".claude" / "skills" / skill_dir.name
        dest.mkdir(parents=True, exist_ok=True)

        for src_file in skill_dir.iterdir():
            if src_file.is_file() and src_file.suffix == ".md" and not src_file.name.startswith("."):
                shutil.copy2(src_file, dest / src_file.name)

        installed.append(skill_dir.name)

    return installed


def uninstall(cwd: Path) -> dict[str, str]:
    """
    Remove all skill dirs from <cwd>/.claude/skills/.

    Returns dict of skill_name -> "removed" | "skipped".
    """
    skills_root = _skills_root()
    skills = discover_skills(skills_root)
    results = {}

    for skill_dir in skills:
        dest = cwd / ".claude" / "skills" / skill_dir.name
        if dest.exists():
            shutil.rmtree(dest)
            results[skill_dir.name] = "removed"
        else:
            results[skill_dir.name] = "skipped"

    return results
