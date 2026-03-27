"""CLI integration tests: invoke skills and templates as subprocesses."""

import os
import subprocess
import sys
from pathlib import Path

_SRC = str(Path(__file__).parent.parent / "src")


def run_skills(*args: str, cwd_arg: Path | None = None, home: Path | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "cc.skills_cli"]
    if cwd_arg is not None:
        cmd += ["--cwd", str(cwd_arg)]
    cmd += list(args)
    env = {**os.environ, "PYTHONPATH": _SRC}
    if home is not None:
        env["HOME"] = str(home)
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def run_templates(*args: str, cwd_arg: Path | None = None, home: Path | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "cc.templates_cli"]
    if cwd_arg is not None:
        cmd += ["--cwd", str(cwd_arg)]
    cmd += list(args)
    env = {**os.environ, "PYTHONPATH": _SRC}
    if home is not None:
        env["HOME"] = str(home)
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


class TestSkillsInstall:
    def test_install_exits_zero(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_skills("install", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0

    def test_install_creates_user_skills(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", cwd_arg=tmp_path, home=home)
        skills_dir = home / ".claude" / "skills"
        assert skills_dir.is_dir()
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        assert len(skill_dirs) > 0
        for skill_dir in skill_dirs:
            assert (skill_dir / "SKILL.md").exists()

    def test_install_output_lists_skills(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_skills("install", cwd_arg=tmp_path, home=home)
        assert "installed:" in result.stdout

    def test_install_idempotent(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", cwd_arg=tmp_path, home=home)
        result = run_skills("install", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0

    def test_install_no_non_md_files(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", cwd_arg=tmp_path, home=home)
        skills_dir = home / ".claude" / "skills"
        for skill_dir in skills_dir.iterdir():
            for f in skill_dir.iterdir():
                assert f.suffix == ".md", f"unexpected non-.md file: {f}"

    def test_install_project_skill(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_skills("install", "tdd-backend", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0
        assert (tmp_path / ".claude" / "skills" / "tdd-backend" / "SKILL.md").exists()
        assert not (home / ".claude" / "skills" / "tdd-backend").exists()

    def test_install_user_skill_by_name(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_skills("install", "interrogate", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0
        assert (home / ".claude" / "skills" / "interrogate" / "SKILL.md").exists()
        assert not (tmp_path / ".claude" / "skills" / "interrogate").exists()

    def test_install_unknown_skill_fails(self, tmp_path: Path):
        result = run_skills("install", "no-such-skill", cwd_arg=tmp_path)
        assert result.returncode != 0
        assert "unknown skill" in result.stdout


class TestSkillsUninstall:
    def test_uninstall_exits_zero_after_install(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", cwd_arg=tmp_path, home=home)
        result = run_skills("uninstall", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0

    def test_uninstall_removes_skills(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", cwd_arg=tmp_path, home=home)
        run_skills("uninstall", cwd_arg=tmp_path, home=home)
        skills_dir = home / ".claude" / "skills"
        remaining = [d for d in skills_dir.iterdir() if d.is_dir()] if skills_dir.exists() else []
        assert remaining == []

    def test_uninstall_output_lists_skills(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", cwd_arg=tmp_path, home=home)
        result = run_skills("uninstall", cwd_arg=tmp_path, home=home)
        assert "removed:" in result.stdout

    def test_uninstall_clean_dir_exits_zero(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_skills("uninstall", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0

    def test_uninstall_clean_dir_output_has_skipped(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_skills("uninstall", cwd_arg=tmp_path, home=home)
        assert "skipped:" in result.stdout

    def test_uninstall_project_skill(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_skills("install", "tdd-backend", cwd_arg=tmp_path, home=home)
        result = run_skills("uninstall", "tdd-backend", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0
        assert "removed: tdd-backend" in result.stdout
        assert not (tmp_path / ".claude" / "skills" / "tdd-backend").exists()

    def test_uninstall_unknown_skill_fails(self, tmp_path: Path):
        result = run_skills("uninstall", "no-such-skill", cwd_arg=tmp_path)
        assert result.returncode != 0
        assert "unknown skill" in result.stdout


class TestSkillsList:
    def test_list_exits_zero(self):
        result = run_skills("list")
        assert result.returncode == 0

    def test_list_shows_skills_with_scope(self):
        result = run_skills("list")
        assert "interrogate" in result.stdout
        assert "write-prd" in result.stdout
        assert "(user)" in result.stdout
        assert "(project)" in result.stdout


class TestTemplateInit:
    def test_init_exits_zero(self, tmp_path: Path):
        result = run_templates("django", cwd_arg=tmp_path)
        assert result.returncode == 0

    def test_init_creates_claude_md(self, tmp_path: Path):
        run_templates("django", cwd_arg=tmp_path)
        assert (tmp_path / "backend" / "CLAUDE.md").exists()

    def test_init_skips_existing(self, tmp_path: Path):
        target = tmp_path / "backend"
        target.mkdir()
        (target / "CLAUDE.md").write_text("existing")
        result = run_templates("django", cwd_arg=tmp_path)
        assert "skipped" in result.stdout
        assert (target / "CLAUDE.md").read_text() == "existing"

    def test_init_force_overwrites(self, tmp_path: Path):
        target = tmp_path / "backend"
        target.mkdir()
        (target / "CLAUDE.md").write_text("old")
        result = run_templates("django", "--force", cwd_arg=tmp_path)
        assert result.returncode == 0
        assert (target / "CLAUDE.md").read_text() != "old"

    def test_init_custom_path(self, tmp_path: Path):
        result = run_templates("django", "--path", "myapp", cwd_arg=tmp_path)
        assert result.returncode == 0
        assert (tmp_path / "myapp" / "CLAUDE.md").exists()

    def test_init_unknown_template_fails(self, tmp_path: Path):
        result = run_templates("nope", cwd_arg=tmp_path)
        assert result.returncode != 0
        assert "nope" in result.stderr


class TestTemplateList:
    def test_list_exits_zero(self):
        result = run_templates("list")
        assert result.returncode == 0

    def test_list_shows_django(self):
        result = run_templates("list")
        assert "django" in result.stdout
        assert "backend" in result.stdout
