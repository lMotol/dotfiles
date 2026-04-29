from __future__ import annotations

from pathlib import Path

from context import Settings
from installers import SETUP_INSTALLERS, install_system_packages, run_installer
from util import CommandRunner


def ensure_managed_source(shell_rc: Path, block_name: str, source_target: Path) -> None:
    block_start = f"# >>> dotfiles {block_name} >>>"
    block_end = f"# <<< dotfiles {block_name} <<<"
    source_line = f'[ -f "{source_target}" ] && . "{source_target}"'

    shell_rc.parent.mkdir(parents=True, exist_ok=True)
    shell_rc.touch()

    filtered_lines: list[str] = []
    in_block = False
    for line in shell_rc.read_text().splitlines():
        if line == block_start:
            in_block = True
            continue
        if line == block_end:
            in_block = False
            continue
        if not in_block:
            filtered_lines.append(line)

    while filtered_lines and filtered_lines[-1] == "":
        filtered_lines.pop()

    filtered_lines.extend(["", block_start, source_line, block_end])
    shell_rc.write_text("\n".join(filtered_lines) + "\n")


def configure_shell_startup(home: Path, runner: CommandRunner) -> None:
    runner.log("Configuring shell startup files...")
    ensure_managed_source(home / ".zshrc", "zshrc", home / ".config/shell/zshrc")
    ensure_managed_source(home / ".bashrc", "bashrc", home / ".config/shell/bashrc")
    ensure_managed_source(home / ".bash_profile", "bash login", home / ".bashrc")


def should_skip_dotfile(name: str) -> bool:
    return name in {".beads", ".git", ".github", ".gitignore", ".gitmodules", ".setup-venv"}


def symlink_path(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink() or destination.is_file():
        destination.unlink()
    elif destination.exists():
        raise RuntimeError(f"Cannot replace existing directory: {destination}")

    destination.symlink_to(source)


def link_dotfiles(source: Path, destination: Path) -> None:
    if source.is_dir():
        if destination.is_symlink() and destination.resolve() == source.resolve():
            destination.unlink()

        destination.mkdir(parents=True, exist_ok=True)
        for child in sorted(source.iterdir()):
            link_dotfiles(child, destination / child.name)
        return

    symlink_path(source, destination)


def create_dotfile_links(context: Settings, runner: CommandRunner) -> None:
    runner.log("")
    runner.log("===================================")
    runner.log("Creating dotfile symlinks...")
    runner.log("===================================")

    for dotfile in sorted(context.root.iterdir()):
        if not dotfile.name.startswith("."):
            continue
        if should_skip_dotfile(dotfile.name):
            continue
        runner.log(f"Linking {dotfile.name}...")
        link_dotfiles(dotfile, context.home / dotfile.name)


def run_setup(context: Settings, runner: CommandRunner) -> int:
    if context.os_name == "unknown":
        raise RuntimeError("Unsupported OS")

    runner.log("===================================")
    runner.log("Dotfiles Setup Script")
    runner.log(f"Dotfiles dir: {context.root}")
    runner.log(f"OS: {context.os_name}")
    runner.log(f"CI: {str(context.ci).lower()}")
    runner.log("===================================")

    install_system_packages(context, runner)

    runner.log("")
    runner.log("Running installation scripts...")
    for installer_name in SETUP_INSTALLERS:
        runner.log("")
        runner.log(f"Executing: {installer_name}")
        try:
            run_installer(installer_name, context, runner)
        except Exception as exc:  # noqa: BLE001
            if context.strict_install_scripts:
                raise
            runner.log(f"Warning: {installer_name} failed, continuing... ({exc})")

    create_dotfile_links(context, runner)
    configure_shell_startup(context.home, runner)

    runner.log("")
    runner.log("===================================")
    runner.log("Setup Complete!")
    runner.log("===================================")
    runner.log("")
    runner.log("Next steps:")
    runner.log("  1. Reload your shell: exec $SHELL -l")
    runner.log("  2. Start tmux and press 'prefix + I' to install tmux plugins")
    return 0
