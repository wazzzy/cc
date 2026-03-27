"""Tests for the templates installer (claude-md init behaviour)."""

from pathlib import Path
from unittest.mock import patch

import pytest

import templates.installer as _mod
from templates.installer import init, list_templates, discover_templates, parse_template_meta, _templates_root


def test_templates_bundled_in_package():
    """Templates must live inside the package dir so they're included when installed via uvx."""
    pkg_dir = Path(_mod.__file__).parent
    found = discover_templates(pkg_dir)
    assert len(found) > 0, "no templates found inside package dir"


def _make_template(root: Path, name: str, default_path: str | None = None) -> Path:
    """Helper: create a fake template dir with TEMPLATE.md and CLAUDE.md."""
    tpl = root / name
    tpl.mkdir()
    dp = default_path or name
    (tpl / "TEMPLATE.md").write_text(f"---\nname: {name}\ndefault_path: {dp}\n---\n")
    (tpl / "CLAUDE.md").write_text(f"# {name.capitalize()} template")
    return tpl


@pytest.fixture()
def fake_templates_root(tmp_path: Path) -> Path:
    """Create a fake templates root with one template."""
    _make_template(tmp_path, "django", default_path="backend")
    # Dir without TEMPLATE.md — should be ignored
    other = tmp_path / "not-a-template"
    other.mkdir()
    (other / "readme.md").write_text("not a template")
    return tmp_path


def _patch_root(fake_root: Path):
    return patch("templates.installer._templates_root", return_value=fake_root)


class TestParseTemplateMeta:
    def test_reads_default_path(self, tmp_path: Path):
        d = _make_template(tmp_path, "django", default_path="backend")
        assert parse_template_meta(d)["default_path"] == "backend"

    def test_reads_name(self, tmp_path: Path):
        d = _make_template(tmp_path, "django", default_path="backend")
        assert parse_template_meta(d)["name"] == "django"

    def test_missing_template_md_returns_empty(self, tmp_path: Path):
        d = tmp_path / "s"
        d.mkdir()
        assert parse_template_meta(d) == {}

    def test_no_frontmatter_returns_empty(self, tmp_path: Path):
        d = tmp_path / "s"
        d.mkdir()
        (d / "TEMPLATE.md").write_text("no frontmatter here")
        assert parse_template_meta(d) == {}


class TestListTemplates:
    def test_returns_name_and_default_path(self, fake_templates_root: Path):
        with _patch_root(fake_templates_root):
            result = list_templates()
        assert ("django", "backend") in result

    def test_does_not_include_non_templates(self, fake_templates_root: Path):
        with _patch_root(fake_templates_root):
            names = [n for n, _ in list_templates()]
        assert "not-a-template" not in names


class TestInit:
    def test_creates_claude_md(self, fake_templates_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_templates_root):
            status, dest = init(cwd, "django")
        assert status == "created"
        assert dest == cwd / "backend" / "CLAUDE.md"
        assert dest.read_text() == "# Django template"

    def test_creates_target_dir_if_missing(self, fake_templates_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_templates_root):
            init(cwd, "django")
        assert (cwd / "backend").is_dir()

    def test_custom_path(self, fake_templates_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_templates_root):
            status, dest = init(cwd, "django", path="my-app")
        assert dest == cwd / "my-app" / "CLAUDE.md"
        assert dest.exists()

    def test_skips_existing(self, fake_templates_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        target = cwd / "backend"
        target.mkdir(parents=True)
        (target / "CLAUDE.md").write_text("existing content")
        with _patch_root(fake_templates_root):
            status, dest = init(cwd, "django")
        assert status == "skipped"
        assert dest.read_text() == "existing content"

    def test_force_overwrites(self, fake_templates_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        target = cwd / "backend"
        target.mkdir(parents=True)
        (target / "CLAUDE.md").write_text("old content")
        with _patch_root(fake_templates_root):
            status, dest = init(cwd, "django", force=True)
        assert status == "overwritten"
        assert dest.read_text() == "# Django template"

    def test_unknown_template_raises(self, fake_templates_root: Path, tmp_path: Path):
        with _patch_root(fake_templates_root):
            with pytest.raises(ValueError, match="unknown template"):
                init(tmp_path, "nope")

    def test_idempotent_with_force(self, fake_templates_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_templates_root):
            init(cwd, "django")
            status, _ = init(cwd, "django", force=True)
        assert status == "overwritten"
