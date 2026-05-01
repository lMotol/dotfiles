from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
from collections.abc import Callable

from .context import Settings
from .install import fzf, lazygit, npm, nvim, poetry, tpm
from .util import CommandRunner

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

NPM_GLOBAL_PACKAGES = {
    "@beads/bd": "1.0.2",
    "@github/copilot": "0.0.332",
    "@google/gemini-cli": "0.39.1",
    "@openai/codex": "0.123.0",
    "beads-ui": "0.12.0",
    "corepack": "0.29.4",
    "difit": "4.0.3",
    "npm": "11.6.1",
    "opencode-ai": "1.14.31",
    "tree-sitter-cli": "0.26.8",
}

SETUP_INSTALLERS = ("fzf", "lazygit", "npm", "nvim", "tpm")


def _nvm_dir(context: Settings) -> Path:
    return context.home / ".nvm"


def _npm_shell_prefix(context: Settings) -> str:
    nvm_dir = shlex.quote(str(_nvm_dir(context)))
    return f"export NVM_DIR={nvm_dir}; [ -s \"$NVM_DIR/nvm.sh\" ] && . \"$NVM_DIR/nvm.sh\"; "


def _load_installed_npm_packages(context: Settings, runner: CommandRunner) -> dict[str, str]:
    command = _npm_shell_prefix(context) + "npm list -g --depth=0 --json"
    completed = runner.run(["bash", "-lc", command], capture_output=True)
    payload = json.loads(completed.stdout)
    dependencies = payload.get("dependencies", {})
    return {
        package_name: str(package_meta.get("version", ""))
        for package_name, package_meta in dependencies.items()
        if isinstance(package_meta, dict)
    }


def install_npm_global_packages(
    context: Settings,
    runner: CommandRunner,
    package_names: tuple[str, ...] | None = None,
) -> None:
    selected_names = package_names or tuple(NPM_GLOBAL_PACKAGES)
    selected_specs = {name: NPM_GLOBAL_PACKAGES[name] for name in selected_names}

    installed_packages = _load_installed_npm_packages(context, runner)
    missing_specs = [
        f"{package_name}@{version}"
        for package_name, version in selected_specs.items()
        if installed_packages.get(package_name) != version
    ]

    if not missing_specs:
        runner.log("npm global packages are already installed at the requested versions")
        return

    runner.log("Installing npm global packages...")
    command = _npm_shell_prefix(context) + "npm install -g " + " ".join(shlex.quote(spec) for spec in missing_specs)
    runner.run(["bash", "-lc", command])


def install_codex_cli(context: Settings, runner: CommandRunner) -> None:
    install_npm_global_packages(context, runner, ("@openai/codex",))


def install_tree_sitter_cli(context: Settings, runner: CommandRunner) -> None:
    install_npm_global_packages(context, runner, ("tree-sitter-cli",))


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
    "codex": install_codex_cli,
    "fzf": fzf.install_tool,
    "lazygit": lazygit.install_tool,
    "npm": npm.install_tool,
    "tree-sitter": install_tree_sitter_cli,
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
