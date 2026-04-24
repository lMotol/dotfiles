from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Sequence

from .context import AppContext
from .installers import INSTALLER_FUNCTIONS, run_installer
from .setup_flow import run_setup
from .shell import CommandRunner

ROOT = Path(__file__).resolve().parents[1]


def add_common_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--os", dest="os_name", choices=["linux", "macos"], help="override detected OS")
    parser.add_argument("--ci", action="store_true", help="force CI mode")
    parser.add_argument("--skip-system-packages", action="store_true", help="skip apt/brew package installation")
    parser.add_argument("--strict-install-scripts", action="store_true", help="fail fast when an installer fails")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="dotfiles management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    detect_parser = subparsers.add_parser("detect-os", help="print detected OS")
    add_common_flags(detect_parser)

    install_parser = subparsers.add_parser("install", help="run a single installer")
    install_parser.add_argument("target", choices=sorted(INSTALLER_FUNCTIONS))
    add_common_flags(install_parser)

    setup_parser = subparsers.add_parser("setup", help="run full setup")
    add_common_flags(setup_parser)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    context = AppContext.from_args(args, ROOT)
    runner = CommandRunner()

    try:
        if args.command == "detect-os":
            print(context.os_name)
            return 0
        if args.command == "install":
            run_installer(args.target, context, runner)
            return 0
        if args.command == "setup":
            return int(run_setup(context, runner))
    except RuntimeError as exc:
        runner.log(f"Error: {exc}")
        return 1
    except subprocess.CalledProcessError as exc:
        runner.log(f"Command failed with exit code {exc.returncode}: {runner.quote_command(exc.cmd if isinstance(exc.cmd, Sequence) else [str(exc.cmd)])}")
        return exc.returncode

    parser.error(f"Unknown command: {args.command}")
    return 2
