#!/usr/bin/env python3

from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[2]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

from script.context import Settings
from script.util import CommandRunner

from script.install._script import run_install_script


def install_tool(context: Settings, runner: CommandRunner) -> None:
    poetry_bin = context.home / ".local/bin/poetry"
    if runner.command_exists("poetry"):
        runner.log(f"Poetry is already installed ({runner.command_first_line(['poetry', '--version'])})")
        return
    if poetry_bin.exists():
        runner.log(f"Poetry is already installed ({runner.command_first_line([str(poetry_bin), '--version'])})")
        return

    runner.log("Installing Poetry...")
    runner.run_shell("curl -sSL https://install.python-poetry.org | python3 -")

    if poetry_bin.exists():
        runner.log(runner.command_first_line([str(poetry_bin), "--version"]))
    runner.log("Poetry installation complete!")
    runner.log("Please reload your shell: exec $SHELL -l")


if __name__ == "__main__":
    raise SystemExit(run_install_script("poetry"))
