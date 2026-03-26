"""CLI integration tests: invoke skills as a subprocess against a temp dir."""

import os
import subprocess
import sys
from pathlib import Path

_SRC = str(Path(__file__).parent.parent / "src")


def run_cli(*args: str, cwd_arg: Path | None = None, home: Path | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "skills.cli"]
    if cwd_arg is not None:
        cmd += ["--cwd", str(cwd_arg)]
    cmd += list(args)
    env = {**os.environ, "PYTHONPATH": _SRC}
    if home is not None:
        env["HOME"] = str(home)
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


class TestCLIInstall:
    def test_install_exits_zero(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_cli("install", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0

    def test_install_creates_user_skills(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_cli("install", cwd_arg=tmp_path, home=home)
        skills_dir = home / ".claude" / "skills"
        assert skills_dir.is_dir()
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        assert len(skill_dirs) > 0
        for skill_dir in skill_dirs:
            assert (skill_dir / "SKILL.md").exists()

    def test_install_output_lists_skills(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_cli("install", cwd_arg=tmp_path, home=home)
        assert "installed:" in result.stdout

    def test_install_idempotent(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_cli("install", cwd_arg=tmp_path, home=home)
        result = run_cli("install", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0

    def test_install_no_non_md_files(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_cli("install", cwd_arg=tmp_path, home=home)
        skills_dir = home / ".claude" / "skills"
        for skill_dir in skills_dir.iterdir():
            for f in skill_dir.iterdir():
                assert f.suffix == ".md", f"unexpected non-.md file: {f}"


class TestCLIUninstall:
    def test_uninstall_exits_zero_after_install(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_cli("install", cwd_arg=tmp_path, home=home)
        result = run_cli("uninstall", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0

    def test_uninstall_removes_skills(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_cli("install", cwd_arg=tmp_path, home=home)
        run_cli("uninstall", cwd_arg=tmp_path, home=home)
        skills_dir = home / ".claude" / "skills"
        remaining = [d for d in skills_dir.iterdir() if d.is_dir()] if skills_dir.exists() else []
        assert remaining == []

    def test_uninstall_output_lists_skills(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_cli("install", cwd_arg=tmp_path, home=home)
        result = run_cli("uninstall", cwd_arg=tmp_path, home=home)
        assert "removed:" in result.stdout

    def test_uninstall_clean_dir_exits_zero(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_cli("uninstall", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0

    def test_uninstall_clean_dir_output_has_skipped(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_cli("uninstall", cwd_arg=tmp_path, home=home)
        assert "skipped:" in result.stdout


class TestCLIList:
    def test_list_exits_zero(self):
        result = run_cli("list")
        assert result.returncode == 0

    def test_list_shows_skills(self):
        result = run_cli("list")
        assert "interrogate" in result.stdout
        assert "write-prd" in result.stdout


class TestCLISelective:
    def test_install_project_skill(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_cli("install", "tdd-backend", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0
        assert (tmp_path / ".claude" / "skills" / "tdd-backend" / "SKILL.md").exists()
        # Should NOT be in home
        assert not (home / ".claude" / "skills" / "tdd-backend").exists()

    def test_install_user_skill_by_name(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        result = run_cli("install", "interrogate", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0
        assert (home / ".claude" / "skills" / "interrogate" / "SKILL.md").exists()
        # Should NOT be in cwd
        assert not (tmp_path / ".claude" / "skills" / "interrogate").exists()

    def test_install_unknown_skill_fails(self, tmp_path: Path):
        result = run_cli("install", "no-such-skill", cwd_arg=tmp_path)
        assert result.returncode != 0
        assert "unknown skill" in result.stdout

    def test_uninstall_project_skill(self, tmp_path: Path):
        home = tmp_path / "home"
        home.mkdir()
        run_cli("install", "tdd-backend", cwd_arg=tmp_path, home=home)
        result = run_cli("uninstall", "tdd-backend", cwd_arg=tmp_path, home=home)
        assert result.returncode == 0
        assert "removed: tdd-backend" in result.stdout
        assert not (tmp_path / ".claude" / "skills" / "tdd-backend").exists()

    def test_uninstall_unknown_skill_fails(self, tmp_path: Path):
        result = run_cli("uninstall", "no-such-skill", cwd_arg=tmp_path)
        assert result.returncode != 0
        assert "unknown skill" in result.stdout
