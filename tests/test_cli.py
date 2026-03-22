"""CLI integration tests: invoke skills as a subprocess against a temp dir."""

import os
import subprocess
import sys
from pathlib import Path

_SRC = str(Path(__file__).parent.parent / "src")


def run_cli(*args: str, cwd_arg: Path | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "skills.cli"]
    if cwd_arg is not None:
        cmd += ["--cwd", str(cwd_arg)]
    cmd += list(args)
    env = {**os.environ, "PYTHONPATH": _SRC}
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


class TestCLIInstall:
    def test_install_exits_zero(self, tmp_path: Path):
        result = run_cli("install", cwd_arg=tmp_path)
        assert result.returncode == 0

    def test_install_creates_skills(self, tmp_path: Path):
        run_cli("install", cwd_arg=tmp_path)
        skills_dir = tmp_path / ".claude" / "skills"
        assert skills_dir.is_dir()
        # At least one skill dir with a SKILL.md should exist
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        assert len(skill_dirs) > 0
        for skill_dir in skill_dirs:
            assert (skill_dir / "SKILL.md").exists()

    def test_install_output_lists_skills(self, tmp_path: Path):
        result = run_cli("install", cwd_arg=tmp_path)
        assert "installed:" in result.stdout

    def test_install_idempotent(self, tmp_path: Path):
        run_cli("install", cwd_arg=tmp_path)
        result = run_cli("install", cwd_arg=tmp_path)
        assert result.returncode == 0

    def test_install_no_non_md_files(self, tmp_path: Path):
        run_cli("install", cwd_arg=tmp_path)
        skills_dir = tmp_path / ".claude" / "skills"
        for skill_dir in skills_dir.iterdir():
            for f in skill_dir.iterdir():
                assert f.suffix == ".md", f"unexpected non-.md file: {f}"


class TestCLIUninstall:
    def test_uninstall_exits_zero_after_install(self, tmp_path: Path):
        run_cli("install", cwd_arg=tmp_path)
        result = run_cli("uninstall", cwd_arg=tmp_path)
        assert result.returncode == 0

    def test_uninstall_removes_skills(self, tmp_path: Path):
        run_cli("install", cwd_arg=tmp_path)
        run_cli("uninstall", cwd_arg=tmp_path)
        skills_dir = tmp_path / ".claude" / "skills"
        remaining = [d for d in skills_dir.iterdir() if d.is_dir()] if skills_dir.exists() else []
        assert remaining == []

    def test_uninstall_output_lists_skills(self, tmp_path: Path):
        run_cli("install", cwd_arg=tmp_path)
        result = run_cli("uninstall", cwd_arg=tmp_path)
        assert "removed:" in result.stdout

    def test_uninstall_clean_dir_exits_zero(self, tmp_path: Path):
        result = run_cli("uninstall", cwd_arg=tmp_path)
        assert result.returncode == 0

    def test_uninstall_clean_dir_output_has_skipped(self, tmp_path: Path):
        result = run_cli("uninstall", cwd_arg=tmp_path)
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
    def _first_skill(self, tmp_path: Path) -> str:
        result = run_cli("install", cwd_arg=tmp_path)
        skills_dir = tmp_path / ".claude" / "skills"
        return sorted(d.name for d in skills_dir.iterdir() if d.is_dir())[0]

    def test_install_single_skill(self, tmp_path: Path):
        skill = self._first_skill(tmp_path)
        tmp2 = tmp_path / "proj2"
        tmp2.mkdir()
        result = run_cli("install", skill, cwd_arg=tmp2)
        assert result.returncode == 0
        skills_dir = tmp2 / ".claude" / "skills"
        installed = [d.name for d in skills_dir.iterdir() if d.is_dir()]
        assert installed == [skill]

    def test_install_unknown_skill_fails(self, tmp_path: Path):
        result = run_cli("install", "no-such-skill", cwd_arg=tmp_path)
        assert result.returncode != 0
        assert "unknown skill" in result.stdout

    def test_uninstall_single_skill(self, tmp_path: Path):
        skill = self._first_skill(tmp_path)
        result = run_cli("uninstall", skill, cwd_arg=tmp_path)
        assert result.returncode == 0
        assert f"removed: {skill}" in result.stdout
        assert not (tmp_path / ".claude" / "skills" / skill).exists()

    def test_uninstall_unknown_skill_fails(self, tmp_path: Path):
        result = run_cli("uninstall", "no-such-skill", cwd_arg=tmp_path)
        assert result.returncode != 0
        assert "unknown skill" in result.stdout
