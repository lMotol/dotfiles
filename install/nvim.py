#!/usr/bin/env python3

from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

import tempfile
from pathlib import Path

from context import Settings
from util import CommandRunner

from install._script import run_install_script


def install_tool(context: Settings, runner: CommandRunner) -> None:
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


if __name__ == "__main__":
    raise SystemExit(run_install_script("nvim"))
