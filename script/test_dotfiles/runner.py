from __future__ import annotations

import contextlib
from datetime import datetime
import os
from pathlib import Path
import subprocess
import sys

from script.util import quote_command

IMAGE_NAME = "dotfiles-linux-test"


class Tee:
    def __init__(self, *streams) -> None:
        self._streams = streams

    def write(self, data: str) -> int:
        for stream in self._streams:
            stream.write(data)
            stream.flush()
        return len(data)

    def flush(self) -> None:
        for stream in self._streams:
            stream.flush()


def _stream_command(command: list[str], *, cwd: Path | None = None) -> None:
    print(f"+ {quote_command(command)}")
    process = subprocess.Popen(
        command,
        cwd=str(cwd) if cwd is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="")
    returncode = process.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, command)


def _run_interactive_command(command: list[str], *, cwd: Path | None = None) -> None:
    print(f"+ {quote_command(command)}")
    subprocess.run(command, check=True, cwd=str(cwd) if cwd is not None else None)


def run_smoke_test(repo_root: Path, *, interactive: bool = False) -> int:
    test_dir = repo_root / "script/test_dotfiles"
    log_dir = test_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"setup-smoke-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"

    if interactive and (not sys.stdin.isatty() or not sys.stdout.isatty()):
        raise RuntimeError("Interactive smoke test requires a TTY")

    with log_file.open("w") as file_handle:
        tee = Tee(file_handle, sys.stdout)
        with contextlib.redirect_stdout(tee), contextlib.redirect_stderr(tee):
            print(f"Writing smoke test log to {log_file}")
            print(f"Building Docker image {IMAGE_NAME} from {repo_root}")
            _stream_command(["docker", "build", "-t", IMAGE_NAME, "-f", str(test_dir / "Dockerfile"), str(repo_root)])
            docker_run = [
                "docker",
                "run",
                "--rm",
                "--user",
                f"{os.getuid()}:{os.getgid()}",
                "-e",
                "HOME=/tmp/dotfiles-test-home",
                "-v",
                f"{repo_root}:/workspace:ro",
            ]
            if interactive:
                docker_run.extend(["-it", IMAGE_NAME, "--interactive"])
                print("Running setup smoke test in Docker and opening an interactive shell")
                print("The interactive session output is not mirrored into the smoke-test log.")
                _run_interactive_command(docker_run)
            else:
                docker_run.append(IMAGE_NAME)
                print("Running setup smoke test in Docker")
                _stream_command(docker_run)

    return 0


if __name__ == "__main__":
    raise SystemExit(run_smoke_test(Path(__file__).resolve().parents[2]))
