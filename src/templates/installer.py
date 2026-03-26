"""Template installer: copies CLAUDE.md templates into target directories."""

import shutil
from pathlib import Path

# Default target paths relative to cwd for each template.
DEFAULT_PATHS: dict[str, str] = {
    "django": "backend",
}


def _templates_root() -> Path:
    """Return the directory containing all template folders (the package dir)."""
    return Path(__file__).parent


def discover_templates(templates_root: Path) -> list[Path]:
    """Return all template dirs (top-level dirs containing CLAUDE.md)."""
    return sorted(
        d for d in templates_root.iterdir()
        if d.is_dir() and (d / "CLAUDE.md").exists()
    )


def list_templates() -> list[tuple[str, str]]:
    """Return (name, default_path) for all available templates."""
    return [
        (d.name, DEFAULT_PATHS.get(d.name, d.name))
        for d in discover_templates(_templates_root())
    ]


def init(cwd: Path, name: str, path: str | None = None, force: bool = False) -> tuple[str, Path]:
    """
    Copy a template's CLAUDE.md into the target directory.

    Returns (status, dest_path) where status is "created", "skipped", or "overwritten".
    Raises ValueError for unknown template name.
    """
    templates_root = _templates_root()
    templates = discover_templates(templates_root)
    known = {d.name: d for d in templates}

    if name not in known:
        available = ", ".join(sorted(known))
        raise ValueError(f"unknown template: {name}. available: {available}")

    target_dir = cwd / (path or DEFAULT_PATHS.get(name, name))
    dest = target_dir / "CLAUDE.md"
    src = known[name] / "CLAUDE.md"

    if dest.exists() and not force:
        return ("skipped", dest)

    status = "overwritten" if dest.exists() else "created"
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return (status, dest)
