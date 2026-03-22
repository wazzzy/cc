"""CLI integration tests: invoke ccskills as a subprocess against a temp dir."""

import os
import subprocess
import sys
from pathlib import Path

_SRC = str(Path(__file__).parent.parent / "src")


def run_cli(*args: str, cwd_arg: Path | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "ccskills.cli"]
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
