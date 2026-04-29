from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Sequence

import typer
from rich.console import Console

from .context import build_settings_from_args
from .installers import INSTALLER_FUNCTIONS, run_installer
from .setup_flow import run_setup
from .test_dotfiles.runner import run_smoke_test
from .util import CommandRunner

ROOT = Path(__file__).resolve().parents[1]

app = typer.Typer(help="dotfiles management CLI")
console = Console()


def _make_args(os: str | None, ci: bool, skip_system_packages: bool, strict_install_scripts: bool) -> object:
    args = type("Args", (), {})()
    args.os_name = os
    args.ci = ci
    args.skip_system_packages = skip_system_packages
    args.strict_install_scripts = strict_install_scripts
    return args


def _make_runner() -> CommandRunner:
    return CommandRunner()


@app.command()
def detect_os(
    os: str | None = typer.Option(None, "--os", "-o", help="override detected OS", show_default=False),
    ci: bool = typer.Option(False, "--ci", help="force CI mode"),
    skip_system_packages: bool = typer.Option(False, "--skip-system-packages", help="skip apt/brew package installation"),
    strict_install_scripts: bool = typer.Option(False, "--strict-install-scripts", help="fail fast when an installer fails"),
):
    """Print detected OS"""
    settings = build_settings_from_args(_make_args(os, ci, skip_system_packages, strict_install_scripts), ROOT)
    console.print(settings.os_name)


@app.command()
def install(
    target: str = typer.Argument(..., help="installer target", autocompletion=lambda: sorted(INSTALLER_FUNCTIONS)),
    os: str | None = typer.Option(None, "--os", "-o", help="override detected OS", show_default=False),
    ci: bool = typer.Option(False, "--ci", help="force CI mode"),
    skip_system_packages: bool = typer.Option(False, "--skip-system-packages", help="skip apt/brew package installation"),
    strict_install_scripts: bool = typer.Option(False, "--strict-install-scripts", help="fail fast when an installer fails"),
):
    """Run a single installer"""
    settings = build_settings_from_args(_make_args(os, ci, skip_system_packages, strict_install_scripts), ROOT)
    runner = _make_runner()
    try:
        run_installer(target, settings, runner)
    except RuntimeError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1)
    except subprocess.CalledProcessError as exc:
        console.print(f"[red]Command failed with exit code {exc.returncode}[/red]")
        raise typer.Exit(code=exc.returncode)


@app.command()
def setup(
    os: str | None = typer.Option(None, "--os", "-o", help="override detected OS", show_default=False),
    ci: bool = typer.Option(False, "--ci", help="force CI mode"),
    skip_system_packages: bool = typer.Option(False, "--skip-system-packages", help="skip apt/brew package installation"),
    strict_install_scripts: bool = typer.Option(False, "--strict-install-scripts", help="fail fast when an installer fails"),
):
    """Run full setup"""
    settings = build_settings_from_args(_make_args(os, ci, skip_system_packages, strict_install_scripts), ROOT)
    runner = _make_runner()
    try:
        result = run_setup(settings, runner)
        raise typer.Exit(code=int(result))
    except RuntimeError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1)
    except subprocess.CalledProcessError as exc:
        console.print(f"[red]Command failed with exit code {exc.returncode}[/red]")
        raise typer.Exit(code=exc.returncode)


@app.command()
def test() -> None:
    """Run the Linux smoke test in Docker."""
    try:
        raise typer.Exit(code=run_smoke_test(ROOT))
    except subprocess.CalledProcessError as exc:
        console.print(f"[red]Command failed with exit code {exc.returncode}[/red]")
        raise typer.Exit(code=exc.returncode)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        app(args=list(argv) if argv is not None else None, standalone_mode=False)
        return 0
    except typer.Exit as exc:
        return exc.exit_code or 0
