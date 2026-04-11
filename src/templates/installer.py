"""Templates installer: copies CLAUDE.md templates into target directories."""

import shutil
from pathlib import Path


def _templates_root() -> Path:
    """Return the directory containing all template folders (the package dir)."""
    return Path(__file__).parent


def parse_template_meta(template_dir: Path) -> dict[str, str]:
    """Read TEMPLATE.md frontmatter and return metadata as a dict."""
    template_md = template_dir / "TEMPLATE.md"
    if not template_md.exists():
        return {}
    text = template_md.read_text()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip()
    return meta


def discover_templates(templates_root: Path) -> list[Path]:
    """Return all template dirs (top-level dirs containing TEMPLATE.md and CLAUDE.md)."""
    return sorted(
        d for d in templates_root.iterdir()
        if d.is_dir() and (d / "TEMPLATE.md").exists() and (d / "CLAUDE.md").exists()
    )


def list_templates() -> list[tuple[str, str]]:
    """Return (name, default_path) for all available templates."""
    return [
        (d.name, parse_template_meta(d).get("default_path", d.name))
        for d in discover_templates(_templates_root())
    ]


def init(cwd: Path, name: str, path: str | None = None, force: bool = False, target: str = "claude") -> tuple[str, Path]:
    """
    Copy a template's CLAUDE.md (and any companion .md files) into the target directory.

    Returns (status, dest_path) where status is "created", "skipped", or "overwritten".
    Raises ValueError for unknown template name.
    The `target` parameter ("claude" or "pi") is accepted for CLI consistency; the
    destination path is the same for both since CLAUDE.md lives in the project tree.
    """
    templates_root = _templates_root()
    templates = discover_templates(templates_root)
    known = {d.name: d for d in templates}

    if name not in known:
        available = ", ".join(sorted(known))
        raise ValueError(f"unknown template: {name}. available: {available}")

    meta = parse_template_meta(known[name])
    default_path = meta.get("default_path", name)
    target_dir = cwd / (path or default_path)
    dest = target_dir / "CLAUDE.md"

    if dest.exists() and not force:
        return ("skipped", dest)

    status = "overwritten" if dest.exists() else "created"
    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy CLAUDE.md and all companion .md files referenced alongside it
    template_dir = known[name]
    for src_file in sorted(template_dir.iterdir()):
        if src_file.is_file() and src_file.suffix == ".md" and src_file.name != "TEMPLATE.md":
            shutil.copy2(src_file, target_dir / src_file.name)

    return (status, dest)
