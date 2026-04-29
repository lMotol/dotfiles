#!/usr/bin/env python3

from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[2]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

import os
import shlex
from pathlib import Path

from script.context import Settings
from script.util import CommandRunner

from script.install._script import run_install_script


def install_tool(context: Settings, runner: CommandRunner) -> None:
    if runner.command_exists("npm"):
        runner.log(f"npm is already installed (version: {runner.command_first_line(['npm', '-v'])})")
        return

    nvm_dir = Path(os.environ.get("NVM_DIR", str(context.home / ".nvm")))
    if not (nvm_dir / "nvm.sh").exists():
        runner.log("Installing nvm...")
        runner.run_shell("PROFILE=/dev/null curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash")

    if not (nvm_dir / "nvm.sh").exists():
        raise RuntimeError("nvm is not available after installation")

    shell_command = (
        f"export NVM_DIR={shlex.quote(str(nvm_dir))}; "
        "[ -s \"$NVM_DIR/nvm.sh\" ] && . \"$NVM_DIR/nvm.sh\"; "
        "nvm install --lts; "
        "nvm alias default 'lts/*'; "
        "nvm use --lts; "
        "npm -v"
    )
    runner.log("Installing Node.js LTS via nvm...")
    runner.run_shell(shell_command)
    runner.log("npm has been installed successfully!")


if __name__ == "__main__":
    raise SystemExit(run_install_script("npm"))
