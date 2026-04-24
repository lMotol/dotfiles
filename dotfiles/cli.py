from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Sequence

import typer
from rich.console import Console

from .context import build_settings_from_args, Settings
from .installers import INSTALLER_FUNCTIONS, run_installer
from .setup_flow import run_setup
from .shell import CommandRunner

ROOT = Path(__file__).resolve().parents[1]

app = typer.Typer(help="dotfiles management CLI")
console = Console()


def _make_runner() -> CommandRunner:
    # central place to create the command runner; keep it lightweight
    return CommandRunner()


@app.command()
def detect_os(
    os: str | None = typer.Option(None, "--os", "-o", help="override detected OS", show_default=False),
    ci: bool = typer.Option(False, "--ci", help="force CI mode"),
    skip_system_packages: bool = typer.Option(False, "--skip-system-packages", help="skip apt/brew package installation"),
    strict_install_scripts: bool = typer.Option(False, "--strict-install-scripts", help="fail fast when an installer fails"),
):
    """Print detected OS"""
    # Typer gives us plain values here; wrap them in the same lightweight
    # object shape the rest of the CLI uses before handing off to Settings.
    class _A:
        pass

    a = _A()
    a.os_name = os
    a.ci = ci
    a.skip_system_packages = skip_system_packages
    a.strict_install_scripts = strict_install_scripts
    settings = build_settings_from_args(a, ROOT)
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
    a = type("_A", (), {})()
    a.os_name = os
    a.ci = ci
    a.skip_system_packages = skip_system_packages
    a.strict_install_scripts = strict_install_scripts
    settings = build_settings_from_args(a, ROOT)
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
    a = type("_A", (), {})()
    a.os_name = os
    a.ci = ci
    a.skip_system_packages = skip_system_packages
    a.strict_install_scripts = strict_install_scripts
    settings = build_settings_from_args(a, ROOT)
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


def main(argv: Sequence[str] | None = None) -> int:
    """Compatibility wrapper that preserves the previous main signature.

    Returns an exit code so existing entrypoints keep working.
    """
    try:
        app(args=list(argv) if argv is not None else None, standalone_mode=False)
        return 0
    except typer.Exit as e:
        return e.exit_code or 0
