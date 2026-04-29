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

from script.context import Settings
from script.util import CommandRunner

from script.install._script import run_install_script


def install_tool(context: Settings, runner: CommandRunner) -> None:
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


if __name__ == "__main__":
    raise SystemExit(run_install_script("lazygit"))
