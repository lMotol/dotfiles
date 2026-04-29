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
    target_dir = context.home / ".tmux/plugins/tpm"
    if target_dir.exists():
        if (target_dir / ".git").is_dir():
            runner.log("Updating tpm...")
            runner.run(["git", "-C", str(target_dir), "pull", "--ff-only", "origin", "master"])
        else:
            raise RuntimeError(f"{target_dir} exists but is not a git repository")
    else:
        runner.log("Installing tpm...")
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        runner.run(["git", "clone", "--depth", "1", "https://github.com/tmux-plugins/tpm", str(target_dir)])

    runner.log("tpm installation complete!")


if __name__ == "__main__":
    raise SystemExit(run_install_script("tpm"))
