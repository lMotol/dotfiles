#!/usr/bin/env python3

from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[2]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

from script.context import Settings
from script.installers import install_tree_sitter_cli
from script.util import CommandRunner

from script.install._script import run_install_script


def install_tool(context: Settings, runner: CommandRunner) -> None:
    install_tree_sitter_cli(context, runner)


if __name__ == "__main__":
    raise SystemExit(run_install_script("tree-sitter"))
