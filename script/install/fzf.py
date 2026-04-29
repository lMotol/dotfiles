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
    fzf_dir = context.home / ".fzf"
    if fzf_dir.exists():
        if (fzf_dir / ".git").is_dir():
            runner.log("Updating fzf...")
            runner.run(["git", "-C", str(fzf_dir), "pull", "--ff-only"])
        else:
            raise RuntimeError(f"{fzf_dir} exists but is not a git repository")
    else:
        runner.log("Installing fzf...")
        runner.run(["git", "clone", "--depth", "1", "https://github.com/junegunn/fzf.git", str(fzf_dir)])

    runner.run([str(fzf_dir / "install"), "--all", "--no-update-rc"])
    runner.log("fzf installation complete!")


if __name__ == "__main__":
    raise SystemExit(run_install_script("fzf"))
