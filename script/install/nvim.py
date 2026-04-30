#!/usr/bin/env python3

from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[2]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

import tempfile
from pathlib import Path
import re
import shutil

from script.context import Settings
from script.util import CommandRunner

from script.install._script import run_install_script


def _parse_nvim_version(version_output: str) -> tuple[int, ...] | None:
    match = re.search(r"NVIM v(\d+(?:\.\d+)*)", version_output)
    if not match:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def _format_version(version: tuple[int, ...]) -> str:
    return ".".join(str(part) for part in version)


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _installed_nvim_command(context: Settings, runner: CommandRunner) -> list[str] | None:
    local_nvim = context.home / ".local/bin/nvim"
    if local_nvim.exists():
        return [str(local_nvim)]

    system_nvim = Path("/usr/local/bin/nvim")
    if system_nvim.exists():
        return [str(system_nvim)]

    if runner.command_exists("nvim"):
        return ["nvim"]

    return None


def install_tool(context: Settings, runner: CommandRunner) -> None:
    if context.os_name == "macos":
        runner.log("macOS detected. Neovim should be installed via Homebrew.")
        return

    latest_release = runner.fetch_json("https://api.github.com/repos/neovim/neovim/releases/latest")
    version = str(latest_release["tag_name"]).removeprefix("v")
    latest_version = tuple(int(part) for part in version.split("."))
    installed_command = _installed_nvim_command(context, runner)

    if installed_command is not None:
        installed_version_line = runner.command_first_line([*installed_command, "--version"])
        installed_version = _parse_nvim_version(installed_version_line)
        if installed_version is not None and installed_version >= latest_version:
            runner.log(f"Neovim is already installed ({installed_version_line})")
            return

        if installed_version is None:
            runner.log(f"Updating Neovim to v{version} (current version could not be parsed: {installed_version_line})")
        else:
            runner.log(f"Updating Neovim from v{_format_version(installed_version)} to v{version}")

    if context.arch in {"x86_64", "i386", "i686"}:
        download_url = f"https://github.com/neovim/neovim/releases/download/v{version}/nvim-linux-x86_64.appimage"
    elif context.arch in {"aarch64", "armv7l", "arm64"}:
        download_url = f"https://github.com/neovim/neovim/releases/download/v{version}/nvim-linux-arm64.appimage"
    else:
        raise RuntimeError(f"Unsupported architecture: {context.arch}")

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        appimage = tmp_dir / "nvim.appimage"
        install_root = context.home / ".local/opt/nvim"
        bin_dir = context.home / ".local/bin"
        nvim_link = bin_dir / "nvim"

        runner.download(download_url, appimage)
        appimage.chmod(0o755)
        runner.run([str(appimage), "--appimage-extract"], cwd=tmp_dir)

        install_root.parent.mkdir(parents=True, exist_ok=True)
        bin_dir.mkdir(parents=True, exist_ok=True)
        _remove_path(install_root)
        _remove_path(nvim_link)
        shutil.move(str(tmp_dir / "squashfs-root"), install_root)
        nvim_link.symlink_to(install_root / "AppRun")

    runner.log("Neovim installation complete!")
    runner.log(runner.command_first_line([str(context.home / ".local/bin/nvim"), "--version"]))


if __name__ == "__main__":
    raise SystemExit(run_install_script("nvim"))
