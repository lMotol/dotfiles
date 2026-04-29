from __future__ import annotations

import json
import shlex
import shutil
import subprocess
import urllib.request
from pathlib import Path
from typing import Sequence


def quote_command(command: Sequence[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def run_command(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    print(f"+ {quote_command(command)}", flush=True)
    return subprocess.run(
        list(command),
        check=True,
        cwd=str(cwd) if cwd is not None else None,
        env=env,
        text=True,
        capture_output=capture_output,
    )


class CommandRunner:
    def log(self, message: str) -> None:
        print(message, flush=True)

    def quote_command(self, command: Sequence[str]) -> str:
        return quote_command(command)

    def run(
        self,
        command: Sequence[str],
        *,
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
        capture_output: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        return run_command(command, cwd=cwd, env=env, capture_output=capture_output)

    def run_shell(
        self,
        command: str,
        *,
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return self.run(["bash", "-lc", command], cwd=cwd, env=env)

    def command_exists(self, name: str) -> bool:
        return shutil.which(name) is not None

    def command_first_line(self, command: Sequence[str]) -> str:
        completed = self.run(command, capture_output=True)
        return completed.stdout.splitlines()[0]

    def fetch_json(self, url: str) -> dict[str, object]:
        request = urllib.request.Request(url, headers={"User-Agent": "dotfiles-cli"})
        with urllib.request.urlopen(request) as response:
            return json.load(response)

    def download(self, url: str, destination: Path) -> None:
        self.log(f"Downloading {url} -> {destination}")
        request = urllib.request.Request(url, headers={"User-Agent": "dotfiles-cli"})
        with urllib.request.urlopen(request) as response, destination.open("wb") as output:
            shutil.copyfileobj(response, output)
