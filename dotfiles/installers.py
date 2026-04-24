from __future__ import annotations

import os
import shlex
import tempfile
from collections.abc import Callable
from pathlib import Path

from .context import AppContext
from .shell import CommandRunner

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


def install_system_packages(context: AppContext, runner: CommandRunner) -> None:
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


def install_codex(context: AppContext, runner: CommandRunner) -> None:
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


def install_fzf(context: AppContext, runner: CommandRunner) -> None:
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


def install_lazygit(context: AppContext, runner: CommandRunner) -> None:
    if context.os_name == "macos":
        runner.log("macOS detected. lazygit should be installed via Homebrew.")
        return

    if runner.command_exists("lazygit"):
        runner.log(f"lazygit is already installed ({runner.command_first_line(['lazygit', '--version'])})")
        return

    if context.arch == "x86_64":
        archive_arch = "x86_64"
    elif context.arch in {"aarch64", "arm64"}:
        archive_arch = "arm64"
    else:
        raise RuntimeError(f"Unsupported architecture: {context.arch}")

    version = str(runner.fetch_json("https://api.github.com/repos/jesseduffield/lazygit/releases/latest")["tag_name"])
    version = version.removeprefix("v")
    download_url = (
        f"https://github.com/jesseduffield/lazygit/releases/download/v{version}/"
        f"lazygit_{version}_Linux_{archive_arch}.tar.gz"
    )

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        tarball = tmp_dir / "lazygit.tar.gz"
        runner.download(download_url, tarball)
        runner.run(["tar", "-C", str(tmp_dir), "-xf", str(tarball), "lazygit"])
        runner.run(["sudo", "install", "-m", "0755", str(tmp_dir / "lazygit"), "/usr/local/bin/lazygit"])

    runner.log("lazygit installation complete!")
    runner.log(runner.command_first_line(["lazygit", "--version"]))


def install_npm(context: AppContext, runner: CommandRunner) -> None:
    if runner.command_exists("npm"):
        runner.log(f"npm is already installed (version: {runner.command_first_line(['npm', '-v'])})")
        return

    nvm_dir = Path(os.environ.get("NVM_DIR", str(context.home / ".nvm")))
    if not (nvm_dir / "nvm.sh").exists():
        runner.log("Installing nvm...")
        runner.run_shell("PROFILE=/dev/null curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash")

    if not (nvm_dir / "nvm.sh").exists():
        raise RuntimeError("nvm is not available after installation")

    shell_command = (
        f"export NVM_DIR={shlex.quote(str(nvm_dir))}; "
        "[ -s \"$NVM_DIR/nvm.sh\" ] && . \"$NVM_DIR/nvm.sh\"; "
        "nvm install --lts; "
        "nvm alias default 'lts/*'; "
        "nvm use --lts; "
        "npm -v"
    )
    runner.log("Installing Node.js LTS via nvm...")
    runner.run_shell(shell_command)
    runner.log("npm has been installed successfully!")


def install_nvim(context: AppContext, runner: CommandRunner) -> None:
    if context.os_name == "macos":
        runner.log("macOS detected. Neovim should be installed via Homebrew.")
        return

    if runner.command_exists("nvim"):
        runner.log(f"Neovim is already installed ({runner.command_first_line(['nvim', '--version'])})")
        return

    if context.arch in {"x86_64", "i386", "i686"}:
        download_url = "https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.appimage"
    elif context.arch in {"aarch64", "armv7l", "arm64"}:
        download_url = "https://github.com/neovim/neovim/releases/latest/download/nvim-linux-arm64.appimage"
    else:
        raise RuntimeError(f"Unsupported architecture: {context.arch}")

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        appimage = tmp_dir / "nvim.appimage"
        runner.download(download_url, appimage)
        appimage.chmod(0o755)
        runner.run([str(appimage), "--appimage-extract"], cwd=tmp_dir)
        runner.run(["sudo", "rm", "-rf", "/opt/nvim"])
        runner.run(["sudo", "mv", str(tmp_dir / "squashfs-root"), "/opt/nvim"])
        runner.run(["sudo", "ln", "-sf", "/opt/nvim/AppRun", "/usr/local/bin/nvim"])

    runner.log("Neovim installation complete!")
    runner.log(runner.command_first_line(["nvim", "--version"]))


def install_poetry(context: AppContext, runner: CommandRunner) -> None:
    poetry_bin = context.home / ".local/bin/poetry"
    if runner.command_exists("poetry"):
        runner.log(f"Poetry is already installed ({runner.command_first_line(['poetry', '--version'])})")
        return
    if poetry_bin.exists():
        runner.log(f"Poetry is already installed ({runner.command_first_line([str(poetry_bin), '--version'])})")
        return

    runner.log("Installing Poetry...")
    runner.run_shell("curl -sSL https://install.python-poetry.org | python3 -")

    if poetry_bin.exists():
        runner.log(runner.command_first_line([str(poetry_bin), "--version"]))
    runner.log("Poetry installation complete!")
    runner.log("Please reload your shell: exec $SHELL -l")


def install_tpm(context: AppContext, runner: CommandRunner) -> None:
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


INSTALLER_FUNCTIONS: dict[str, Callable[[AppContext, CommandRunner], None]] = {
    "codex": install_codex,
    "fzf": install_fzf,
    "lazygit": install_lazygit,
    "npm": install_npm,
    "nvim": install_nvim,
    "poetry": install_poetry,
    "tpm": install_tpm,
}


def run_installer(target: str, context: AppContext, runner: CommandRunner) -> None:
    try:
        installer = INSTALLER_FUNCTIONS[target]
    except KeyError as exc:
        raise RuntimeError(f"Unknown installer: {target}") from exc

    installer(context, runner)
