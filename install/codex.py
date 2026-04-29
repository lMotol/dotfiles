#!/usr/bin/env python3

from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

from context import Settings
from util import CommandRunner

from install._script import run_install_script


def install_tool(context: Settings, runner: CommandRunner) -> None:
    del context
    if runner.command_exists("codex"):
        runner.log(f"Codex CLI is already installed ({runner.command_first_line(['codex', '--version'])})")
        return

    if not runner.command_exists("npm"):
        raise RuntimeError("npm is not installed")

    runner.log("Installing Codex CLI via npm...")
    runner.run(["npm", "install", "-g", "@openai/codex@latest"])

    if runner.command_exists("codex"):
        runner.log("Codex CLI installation successful")
    else:
        runner.log("Installation completed. Please reload your shell.")


if __name__ == "__main__":
    raise SystemExit(run_install_script("codex"))
