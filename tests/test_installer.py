"""Tests for the file installer (install/uninstall behaviour)."""

from pathlib import Path
from unittest.mock import patch

import pytest

import skills.installer as _mod
from skills.installer import install, uninstall, discover_skills, list_skills, parse_scope, _skills_root


def test_skills_bundled_in_package():
    """Skills must live inside the package dir so they're included when installed via uvx."""
    pkg_dir = Path(_mod.__file__).parent
    found = discover_skills(pkg_dir)
    assert len(found) > 0, "no skills found inside package dir — skill dirs must be under src/skills/"


def _make_skill(root: Path, name: str, scope: str = "project", extra_md: bool = True):
    """Helper: create a fake skill dir with given scope."""
    skill_dir = root / name
    skill_dir.mkdir()
    frontmatter = f"---\nname: {name}\nscope: {scope}\ndescription: test\n---\n# {name}"
    (skill_dir / "SKILL.md").write_text(frontmatter)
    if extra_md:
        (skill_dir / "guide.md").write_text("content")
    (skill_dir / "not-markdown.txt").write_text("ignore me")
    (skill_dir / ".hidden.md").write_text("ignore me")
    return skill_dir


@pytest.fixture()
def fake_skills_root(tmp_path: Path) -> Path:
    """Create a fake skills root with user and project scoped skills."""
    _make_skill(tmp_path, "skill-user-a", scope="user")
    _make_skill(tmp_path, "skill-user-b", scope="user")
    _make_skill(tmp_path, "skill-proj", scope="project")
    # Dir WITHOUT SKILL.md — should be ignored
    other = tmp_path / "not-a-skill"
    other.mkdir()
    (other / "readme.md").write_text("not a skill")
    return tmp_path


def _patch_root(fake_root: Path):
    return patch("skills.installer._skills_root", return_value=fake_root)


def _patch_home(home: Path):
    return patch("skills.installer.Path.home", return_value=home)


class TestParseScope:
    def test_reads_user_scope(self, tmp_path: Path):
        d = _make_skill(tmp_path, "s", scope="user")
        assert parse_scope(d) == "user"

    def test_reads_project_scope(self, tmp_path: Path):
        d = _make_skill(tmp_path, "s", scope="project")
        assert parse_scope(d) == "project"

    def test_defaults_to_project(self, tmp_path: Path):
        d = tmp_path / "s"
        d.mkdir()
        (d / "SKILL.md").write_text("---\nname: s\n---\n")
        assert parse_scope(d) == "project"

    def test_no_skill_md(self, tmp_path: Path):
        d = tmp_path / "s"
        d.mkdir()
        assert parse_scope(d) == "project"


class TestListSkills:
    def test_returns_name_and_scope(self, fake_skills_root: Path):
        with _patch_root(fake_skills_root):
            result = list_skills()
        assert ("skill-user-a", "user") in result
        assert ("skill-proj", "project") in result

    def test_does_not_include_non_skills(self, fake_skills_root: Path):
        with _patch_root(fake_skills_root):
            names = [n for n, _ in list_skills()]
        assert "not-a-skill" not in names


class TestInstall:
    def test_bare_install_only_user_scope(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            result = install(cwd)
        names = [n for n, _, _ in result]
        assert "skill-user-a" in names
        assert "skill-user-b" in names
        assert "skill-proj" not in names

    def test_user_skills_go_to_home(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(cwd)
        assert (fake_home / ".claude" / "skills" / "skill-user-a" / "SKILL.md").exists()

    def test_named_project_skill_goes_to_cwd(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(cwd, ["skill-proj"])
        assert (cwd / ".claude" / "skills" / "skill-proj" / "SKILL.md").exists()
        assert not (fake_home / ".claude" / "skills" / "skill-proj").exists()

    def test_copies_md_files(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path)
        assert (fake_home / ".claude" / "skills" / "skill-user-a" / "guide.md").exists()

    def test_skips_non_md_files(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path)
        assert not (fake_home / ".claude" / "skills" / "skill-user-a" / "not-markdown.txt").exists()

    def test_skips_hidden_files(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path)
        assert not (fake_home / ".claude" / "skills" / "skill-user-a" / ".hidden.md").exists()

    def test_skips_dir_without_skill_md(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path)
        assert not (fake_home / ".claude" / "skills" / "not-a-skill").exists()

    def test_returns_tuples(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            result = install(tmp_path)
        for name, scope, dest in result:
            assert isinstance(name, str)
            assert scope in ("user", "project")
            assert isinstance(dest, Path)

    def test_idempotent(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path)
            install(tmp_path)  # second run should not error
        assert (fake_home / ".claude" / "skills" / "skill-user-a" / "SKILL.md").exists()

    def test_install_unknown_raises(self, fake_skills_root: Path, tmp_path: Path):
        with _patch_root(fake_skills_root):
            with pytest.raises(ValueError, match="unknown skill"):
                install(tmp_path, ["nope"])


class TestInstallPi:
    def test_user_skill_goes_to_pi_agent_dir(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path, target="pi")
        assert (fake_home / ".pi" / "agent" / "skills" / "skill-user-a" / "SKILL.md").exists()

    def test_project_skill_goes_to_pi_skills_dir(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(cwd, ["skill-proj"], target="pi")
        assert (cwd / ".pi" / "skills" / "skill-proj" / "SKILL.md").exists()

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


class TestUninstall:
    def test_bare_uninstall_only_user_scope(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(cwd)
            install(cwd, ["skill-proj"])
            results = uninstall(cwd)
        assert "skill-user-a" in results
        assert "skill-user-b" in results
        assert "skill-proj" not in results

    def test_removes_user_skill_from_home(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path)
            uninstall(tmp_path)
        assert not (fake_home / ".claude" / "skills" / "skill-user-a").exists()

    def test_named_uninstall_project_skill(self, fake_skills_root: Path, tmp_path: Path):
        cwd = tmp_path / "project"
        cwd.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(cwd, ["skill-proj"])
            results = uninstall(cwd, ["skill-proj"])
        assert results["skill-proj"] == ("removed", "project")
        assert not (cwd / ".claude" / "skills" / "skill-proj").exists()

    def test_returns_status_and_scope(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            install(tmp_path)
            results = uninstall(tmp_path)
        assert results["skill-user-a"] == ("removed", "user")

    def test_noop_when_not_installed(self, fake_skills_root: Path, tmp_path: Path):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        with _patch_root(fake_skills_root), _patch_home(fake_home):
            results = uninstall(tmp_path)
        assert results["skill-user-a"] == ("skipped", "user")

    def test_uninstall_unknown_raises(self, fake_skills_root: Path, tmp_path: Path):
        with _patch_root(fake_skills_root):
            with pytest.raises(ValueError, match="unknown skill"):
                uninstall(tmp_path, ["nope"])
