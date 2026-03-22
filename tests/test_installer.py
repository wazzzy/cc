"""Tests for the file installer (install/uninstall behaviour)."""

from pathlib import Path
from unittest.mock import patch

import pytest

from skills.installer import install, uninstall


@pytest.fixture()
def fake_skills_root(tmp_path: Path) -> Path:
    """Create a fake skills root with two skills."""
    for skill_name in ("skill-a", "skill-b"):
        skill_dir = tmp_path / skill_name
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(f"# {skill_name}")
        (skill_dir / "guide.md").write_text("content")
        (skill_dir / "not-markdown.txt").write_text("ignore me")
        (skill_dir / ".hidden.md").write_text("ignore me")
    # Also create a dir WITHOUT SKILL.md — should be ignored
    other = tmp_path / "not-a-skill"
    other.mkdir()
    (other / "readme.md").write_text("not a skill")
    return tmp_path


def _patch_root(fake_root: Path):
    return patch("skills.installer._skills_root", return_value=fake_root)


class TestInstall:
    def test_creates_expected_dirs(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            install(cwd)
        assert (cwd / ".claude" / "skills" / "skill-a").is_dir()
        assert (cwd / ".claude" / "skills" / "skill-b").is_dir()

    def test_copies_md_files(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            install(cwd)
        assert (cwd / ".claude" / "skills" / "skill-a" / "SKILL.md").exists()
        assert (cwd / ".claude" / "skills" / "skill-a" / "guide.md").exists()

    def test_skips_non_md_files(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            install(cwd)
        assert not (cwd / ".claude" / "skills" / "skill-a" / "not-markdown.txt").exists()

    def test_skips_hidden_files(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            install(cwd)
        assert not (cwd / ".claude" / "skills" / "skill-a" / ".hidden.md").exists()

    def test_skips_dir_without_skill_md(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            install(cwd)
        assert not (cwd / ".claude" / "skills" / "not-a-skill").exists()

    def test_returns_skill_names(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            result = install(cwd)
        assert sorted(result) == ["skill-a", "skill-b"]

    def test_idempotent(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            install(cwd)
            install(cwd)  # second run should not error
        assert (cwd / ".claude" / "skills" / "skill-a" / "SKILL.md").exists()


class TestUninstall:
    def test_removes_installed_dirs(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            install(cwd)
            uninstall(cwd)
        assert not (cwd / ".claude" / "skills" / "skill-a").exists()
        assert not (cwd / ".claude" / "skills" / "skill-b").exists()

    def test_returns_removed_status(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            install(cwd)
            results = uninstall(cwd)
        assert results["skill-a"] == "removed"
        assert results["skill-b"] == "removed"

    def test_noop_when_not_installed(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            results = uninstall(cwd)  # nothing installed
        assert results["skill-a"] == "skipped"
        assert results["skill-b"] == "skipped"

    def test_noop_does_not_raise(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            uninstall(cwd)  # must not raise


class TestSelectiveInstall:
    def test_install_single(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            result = install(cwd, ["skill-a"])
        assert result == ["skill-a"]
        assert (cwd / ".claude" / "skills" / "skill-a").is_dir()
        assert not (cwd / ".claude" / "skills" / "skill-b").exists()

    def test_install_multiple(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            result = install(cwd, ["skill-a", "skill-b"])
        assert sorted(result) == ["skill-a", "skill-b"]

    def test_install_unknown_raises(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            with pytest.raises(ValueError, match="unknown skill"):
                install(cwd, ["nope"])

    def test_uninstall_single(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            install(cwd)
            results = uninstall(cwd, ["skill-a"])
        assert results == {"skill-a": "removed"}
        assert not (cwd / ".claude" / "skills" / "skill-a").exists()
        assert (cwd / ".claude" / "skills" / "skill-b").exists()

    def test_uninstall_unknown_raises(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        with _patch_root(fake_skills_root):
            with pytest.raises(ValueError, match="unknown skill"):
                uninstall(cwd, ["nope"])
