from __future__ import annotations

import os
from collections.abc import Callable

from context import Settings
from install import codex, fzf, lazygit, npm, nvim, poetry, tpm
from util import CommandRunner

BREW_PACKAGES = [
    "curl",
    "git",
    "ripgrep",
    "tmux",
    "fd",
    "neovim",
    "sheldon",
    "universal-ctags",
    "lazygit",
    "hammerspoon",
]

APT_PACKAGES = [
    "curl",
    "git",
    "ripgrep",
    "build-essential",
    "tmux",
    "fd-find",
    "unzip",
    "universal-ctags",
]

SETUP_INSTALLERS = ("codex", "fzf", "lazygit", "npm", "nvim", "tpm")


def install_system_packages(context: Settings, runner: CommandRunner) -> None:
    if context.skip_system_packages:
        value = os.environ.get("SETUP_SKIP_SYSTEM_PACKAGES", "0")
        runner.log(f"Skipping system package installation (SETUP_SKIP_SYSTEM_PACKAGES={value})")
        return

    if context.os_name == "macos":
        if not runner.command_exists("brew"):
            if context.ci:
                runner.log("Skipping Homebrew installation in CI (should be pre-installed)")
            else:
                runner.log("Installing Homebrew...")
                runner.run_shell("curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | /bin/bash")

        if runner.command_exists("brew"):
            runner.log("Installing packages via Homebrew...")
            runner.run(["brew", "install", *BREW_PACKAGES])
        return

    if context.os_name == "linux":
        if context.ci:
            runner.log("Skipping apt update/upgrade in CI")
        else:
            runner.log("Updating package list...")
            runner.run(["sudo", "apt", "update"])
            runner.run(["sudo", "apt", "upgrade", "-y"])

        runner.log("Installing packages via apt...")
        runner.run(["sudo", "apt-get", "install", "-y", *APT_PACKAGES])
        return

    raise RuntimeError(f"Unsupported OS: {context.os_name}")


INSTALLER_FUNCTIONS: dict[str, Callable[[Settings, CommandRunner], None]] = {
    "codex": codex.install_tool,
    "fzf": fzf.install_tool,
    "lazygit": lazygit.install_tool,
    "npm": npm.install_tool,
    "nvim": nvim.install_tool,
    "poetry": poetry.install_tool,
    "tpm": tpm.install_tool,
}


def run_installer(target: str, context: Settings, runner: CommandRunner) -> None:
    try:
        installer = INSTALLER_FUNCTIONS[target]
    except KeyError as exc:
        raise RuntimeError(f"Unknown installer: {target}") from exc

    installer(context, runner)
