#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parent
INSTALLERS = ("codex", "fzf", "lazygit", "npm", "nvim", "tpm")
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


def log(message: str) -> None:
    print(message, flush=True)


def quote_command(command: Sequence[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def run(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    log(f"$ {quote_command(command)}")
    return subprocess.run(
        list(command),
        check=True,
        cwd=str(cwd) if cwd is not None else None,
        env=env,
        text=True,
        capture_output=capture_output,
    )


def run_shell(command: str, *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return run(["bash", "-lc", command], cwd=cwd, env=env)


def truthy(value: str | None) -> bool:
    return value is not None and value.lower() in {"1", "true", "yes"}


def detect_os_name() -> str:
    platform = os.uname().sysname
    if platform == "Darwin":
        return "macos"
    if platform == "Linux":
        return "linux"
    return "unknown"


def detect_arch() -> str:
    return os.uname().machine


def in_ci() -> bool:
    return truthy(os.environ.get("CI")) or truthy(os.environ.get("GITHUB_ACTIONS"))


def fetch_json(url: str) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"User-Agent": "dotfiles-cli"})
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def download(url: str, destination: Path) -> None:
    log(f"Downloading {url} -> {destination}")
    request = urllib.request.Request(url, headers={"User-Agent": "dotfiles-cli"})
    with urllib.request.urlopen(request) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def command_first_line(command: Sequence[str]) -> str:
    completed = run(command, capture_output=True)
    return completed.stdout.splitlines()[0]


def ensure_managed_source(shell_rc: Path, block_name: str, source_target: Path) -> None:
    block_start = f"# >>> dotfiles {block_name} >>>"
    block_end = f"# <<< dotfiles {block_name} <<<"
    source_line = f'[ -f "{source_target}" ] && . "{source_target}"'

    shell_rc.parent.mkdir(parents=True, exist_ok=True)
    shell_rc.touch()

    lines = shell_rc.read_text().splitlines()
    filtered_lines: list[str] = []
    in_block = False
    for line in lines:
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


def configure_shell_startup(home: Path) -> None:
    log("Configuring shell startup files...")
    ensure_managed_source(home / ".zshrc", "zshrc", home / ".config/shell/zshrc")
    ensure_managed_source(home / ".bashrc", "bashrc", home / ".config/shell/bashrc")
    ensure_managed_source(home / ".bash_profile", "bash login", home / ".bashrc")


def should_skip_dotfile(name: str) -> bool:
    return name in {".beads", ".git", ".github", ".gitignore", ".gitmodules"}


def symlink_path(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink() or destination.is_file():
        destination.unlink()
    elif destination.exists():
        raise RuntimeError(f"Cannot replace existing directory: {destination}")

    destination.symlink_to(source)
    log(f"Linked {destination} -> {source}")


def link_dotfiles(source: Path, destination: Path) -> None:
    if source.is_dir():
        if destination.is_symlink() and destination.resolve() == source.resolve():
            destination.unlink()

        destination.mkdir(parents=True, exist_ok=True)
        for child in sorted(source.iterdir()):
            link_dotfiles(child, destination / child.name)
        return

    symlink_path(source, destination)


def create_dotfile_links(home: Path) -> None:
    log("")
    log("===================================")
    log("Creating dotfile symlinks...")
    log("===================================")

    for dotfile in sorted(ROOT.iterdir()):
        if not dotfile.name.startswith("."):
            continue
        if should_skip_dotfile(dotfile.name):
            continue
        link_dotfiles(dotfile, home / dotfile.name)


def install_system_packages(os_name: str, *, ci: bool, skip_system_packages: bool) -> None:
    if skip_system_packages:
        log(f"Skipping system package installation (SETUP_SKIP_SYSTEM_PACKAGES={os.environ.get('SETUP_SKIP_SYSTEM_PACKAGES', '0')})")
        return

    if os_name == "macos":
        if not command_exists("brew"):
            if ci:
                log("Skipping Homebrew installation in CI (should be pre-installed)")
            else:
                log("Installing Homebrew...")
                run_shell("curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | /bin/bash")

        if command_exists("brew"):
            log("Installing packages via Homebrew...")
            run(["brew", "install", *BREW_PACKAGES])
        return

    if os_name == "linux":
        if ci:
            log("Skipping apt update/upgrade in CI")
            log("Installing packages via apt...")
            try:
                run(["sudo", "apt-get", "install", "-y", *APT_PACKAGES])
            except subprocess.CalledProcessError:
                log("Some packages may already be installed")
        else:
            log("Updating package list...")
            run(["sudo", "apt", "update"])
            run(["sudo", "apt", "upgrade", "-y"])

            log("Installing packages via apt...")
            run(["sudo", "apt-get", "install", "-y", *APT_PACKAGES])
        return

    raise RuntimeError(f"Unsupported OS: {os_name}")


def install_codex(_: argparse.Namespace) -> None:
    tool_name = "Codex CLI"
    if command_exists("codex"):
        log(f"{tool_name} is already installed ({command_first_line(['codex', '--version'])})")
        return

    if not command_exists("npm"):
        raise RuntimeError("npm is not installed")

    log(f"Installing {tool_name} via npm...")
    run(["npm", "install", "-g", "@openai/codex@latest"])

    if command_exists("codex"):
        log(f"{tool_name} installation successful")
    else:
        log("Installation completed. Please reload your shell.")


def install_fzf(args: argparse.Namespace) -> None:
    fzf_dir = args.home / ".fzf"
    if fzf_dir.exists():
        if (fzf_dir / ".git").is_dir():
            log("Updating fzf...")
            run(["git", "-C", str(fzf_dir), "pull", "--ff-only"])
        else:
            raise RuntimeError(f"{fzf_dir} exists but is not a git repository")
    else:
        log("Installing fzf...")
        run(["git", "clone", "--depth", "1", "https://github.com/junegunn/fzf.git", str(fzf_dir)])

    run([str(fzf_dir / "install"), "--all", "--no-update-rc"])
    log("fzf installation complete!")


def install_lazygit(args: argparse.Namespace) -> None:
    if args.os_name == "macos":
        log("macOS detected. lazygit should be installed via Homebrew.")
        return

    if command_exists("lazygit"):
        log(f"lazygit is already installed ({command_first_line(['lazygit', '--version'])})")
        return

    arch = detect_arch()
    if arch == "x86_64":
        lazygit_arch = "x86_64"
    elif arch in {"aarch64", "arm64"}:
        lazygit_arch = "arm64"
    else:
        raise RuntimeError(f"Unsupported architecture: {arch}")

    version = str(fetch_json("https://api.github.com/repos/jesseduffield/lazygit/releases/latest")["tag_name"])
    version = version.removeprefix("v")
    download_url = f"https://github.com/jesseduffield/lazygit/releases/download/v{version}/lazygit_{version}_Linux_{lazygit_arch}.tar.gz"

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        tarball = tmp_dir / "lazygit.tar.gz"
        download(download_url, tarball)
        run(["tar", "-C", str(tmp_dir), "-xf", str(tarball), "lazygit"])
        run(["sudo", "install", "-m", "0755", str(tmp_dir / "lazygit"), "/usr/local/bin/lazygit"])

    log("lazygit installation complete!")
    log(command_first_line(["lazygit", "--version"]))


def install_npm(args: argparse.Namespace) -> None:
    if command_exists("npm"):
        log(f"npm is already installed (version: {command_first_line(['npm', '-v'])})")
        return

    nvm_dir = Path(os.environ.get("NVM_DIR", str(args.home / ".nvm")))
    if not (nvm_dir / "nvm.sh").exists():
        log("Installing nvm...")
        run_shell("PROFILE=/dev/null curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash")

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
    log("Installing Node.js LTS via nvm...")
    run_shell(shell_command)
    log("npm has been installed successfully!")


def install_nvim(args: argparse.Namespace) -> None:
    if args.os_name == "macos":
        log("macOS detected. Neovim should be installed via Homebrew.")
        return

    if command_exists("nvim"):
        log(f"Neovim is already installed ({command_first_line(['nvim', '--version'])})")
        return

    arch = detect_arch()
    if arch in {"x86_64", "i386", "i686"}:
        download_url = "https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.appimage"
    elif arch in {"aarch64", "armv7l", "arm64"}:
        download_url = "https://github.com/neovim/neovim/releases/latest/download/nvim-linux-arm64.appimage"
    else:
        raise RuntimeError(f"Unsupported architecture: {arch}")

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        appimage = tmp_dir / "nvim.appimage"
        download(download_url, appimage)
        appimage.chmod(0o755)
        run([str(appimage), "--appimage-extract"], cwd=tmp_dir)
        run(["sudo", "rm", "-rf", "/opt/nvim"])
        run(["sudo", "mv", str(tmp_dir / "squashfs-root"), "/opt/nvim"])
        run(["sudo", "ln", "-sf", "/opt/nvim/AppRun", "/usr/local/bin/nvim"])

    log("Neovim installation complete!")
    log(command_first_line(["nvim", "--version"]))


def install_tpm(args: argparse.Namespace) -> None:
    target_dir = args.home / ".tmux/plugins/tpm"
    if target_dir.exists():
        if (target_dir / ".git").is_dir():
            log("Updating tpm...")
            run(["git", "-C", str(target_dir), "pull", "--ff-only", "origin", "master"])
        else:
            raise RuntimeError(f"{target_dir} exists but is not a git repository")
    else:
        log("Installing tpm...")
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--depth", "1", "https://github.com/tmux-plugins/tpm", str(target_dir)])

    log("tpm installation complete!")


INSTALLER_FUNCTIONS = {
    "codex": install_codex,
    "fzf": install_fzf,
    "lazygit": install_lazygit,
    "npm": install_npm,
    "nvim": install_nvim,
    "tpm": install_tpm,
}


def run_installer(name: str, args: argparse.Namespace) -> None:
    INSTALLER_FUNCTIONS[name](args)


def print_banner(args: argparse.Namespace) -> None:
    log("===================================")
    log("Dotfiles Setup Script")
    log(f"Dotfiles dir: {ROOT}")
    log(f"OS: {args.os_name}")
    log(f"CI: {str(args.ci).lower()}")
    log("===================================")


def setup(args: argparse.Namespace) -> int:
    if args.os_name == "unknown":
        raise RuntimeError(f"Unsupported OS: {os.uname().sysname}")

    print_banner(args)
    install_system_packages(args.os_name, ci=args.ci, skip_system_packages=args.skip_system_packages)

    log("")
    log("Running installation scripts...")
    for installer in INSTALLERS:
        log("")
        log(f"Executing: {installer}")
        try:
            run_installer(installer, args)
        except Exception as exc:  # noqa: BLE001
            if args.strict_install_scripts:
                raise
            log(f"Warning: {installer} failed, continuing... ({exc})")

    create_dotfile_links(args.home)
    configure_shell_startup(args.home)

    log("")
    log("===================================")
    log("Setup Complete!")
    log("===================================")
    log("")
    log("Next steps:")
    log("  1. Reload your shell: exec $SHELL -l")
    log("  2. Start tmux and press 'prefix + I' to install tmux plugins")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="dotfiles management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    detect_parser = subparsers.add_parser("detect-os", help="print detected OS")
    detect_parser.set_defaults(handler=lambda args: print(args.os_name) or 0)

    install_parser = subparsers.add_parser("install", help="run a single installer")
    install_parser.add_argument("target", choices=sorted(INSTALLER_FUNCTIONS))
    install_parser.set_defaults(handler=lambda args: run_installer(args.target, args) or 0)

    setup_parser = subparsers.add_parser("setup", help="run full setup")
    setup_parser.set_defaults(handler=setup)

    return parser


def enrich_args(args: argparse.Namespace) -> argparse.Namespace:
    args.home = Path(os.environ.get("HOME", str(Path.home()))).expanduser().resolve()
    args.os_name = getattr(args, "os_name", None) or detect_os_name()
    args.ci = getattr(args, "ci", False) or in_ci()
    args.skip_system_packages = getattr(args, "skip_system_packages", False) or truthy(os.environ.get("SETUP_SKIP_SYSTEM_PACKAGES"))
    args.strict_install_scripts = getattr(args, "strict_install_scripts", False) or truthy(os.environ.get("SETUP_STRICT_INSTALL_SCRIPTS"))
    return args


def add_common_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--os", dest="os_name", choices=["linux", "macos"], help="override detected OS")
    parser.add_argument("--ci", action="store_true", help="force CI mode")
    parser.add_argument("--skip-system-packages", action="store_true", help="skip apt/brew package installation")
    parser.add_argument("--strict-install-scripts", action="store_true", help="fail fast when an installer fails")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    for subparser in parser._subparsers._group_actions[0].choices.values():
        add_common_flags(subparser)

    args = enrich_args(parser.parse_args(argv))
    try:
        return int(args.handler(args))
    except RuntimeError as exc:
        log(f"Error: {exc}")
        return 1
    except subprocess.CalledProcessError as exc:
        log(f"Command failed with exit code {exc.returncode}: {quote_command(exc.cmd if isinstance(exc.cmd, Sequence) else [str(exc.cmd)])}")
        return exc.returncode


if __name__ == "__main__":
    sys.exit(main())
