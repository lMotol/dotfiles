from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

if __package__ in {None, ""}:
    import sys

    ROOT = Path(os.environ.get("WORKSPACE_DIR", "/workspace"))
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

from script.test_dotfiles.verify import verify_setup
from script.util import run_command


def _write_stub(path: Path, name: str) -> None:
    path.write_text(
        "#!/usr/bin/env bash\n"
        'if [ "${1:-}" = "--version" ]; then\n'
        f"    printf '{name} test stub\\n'\n"
        "    exit 0\n"
        "fi\n"
        f"printf '{name} test stub\\n'\n"
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main() -> int:
    interactive = "--interactive" in sys.argv[1:]
    workspace_dir = Path(os.environ.get("WORKSPACE_DIR", "/workspace"))
    home = Path(os.environ["HOME"])

    with tempfile.TemporaryDirectory(prefix="dotfiles-linux-test.", dir="/tmp") as repo_dir_name:
        repo_dir = Path(repo_dir_name)
        fake_bin_dir = home / ".local/bin"
        fake_bin_dir.mkdir(parents=True, exist_ok=True)
        _write_stub(fake_bin_dir / "codex", "codex")
        _write_stub(fake_bin_dir / "lazygit", "lazygit")

        shutil.copytree(workspace_dir, repo_dir, symlinks=True, dirs_exist_ok=True)

        env = os.environ.copy()
        env["PATH"] = f"{fake_bin_dir}:{env.get('PATH', '')}"
        env["CI"] = "true"
        env["SETUP_SKIP_SYSTEM_PACKAGES"] = "1"
        env["SETUP_STRICT_INSTALL_SCRIPTS"] = "1"
        for key in ("EDITOR", "VISUAL", "GIT_EDITOR", "FCEDIT", "NVM_DIR"):
            env.pop(key, None)

        run_command(["bash", "-n", str(repo_dir / "setup")], env=env)
        run_command([str(repo_dir / "setup")], env=env)
        run_command([str(repo_dir / "setup")], env=env)

        verify_setup(home, repo_dir)

        if interactive:
            shell = env.get("SHELL") or "/bin/bash"
            print(f"Smoke test passed. Opening interactive shell in {repo_dir}.")
            print(f"HOME={home}")
            print("Exit the shell to finish the test run.")
            subprocess.run([shell], check=True, cwd=repo_dir, env=env)

    print("Setup smoke test completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
