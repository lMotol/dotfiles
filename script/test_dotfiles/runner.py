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


def run_smoke_test(repo_root: Path) -> int:
    test_dir = repo_root / "script/test_dotfiles"
    log_dir = test_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"setup-smoke-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"

    with log_file.open("w") as file_handle:
        tee = Tee(file_handle, sys.stdout)
        with contextlib.redirect_stdout(tee), contextlib.redirect_stderr(tee):
            print(f"Writing smoke test log to {log_file}")
            print(f"Building Docker image {IMAGE_NAME} from {repo_root}")
            _stream_command(["docker", "build", "-t", IMAGE_NAME, "-f", str(test_dir / "Dockerfile"), str(repo_root)])
            print("Running setup smoke test in Docker")
            _stream_command(
                [
                    "docker",
                    "run",
                    "--rm",
                    "--user",
                    f"{os.getuid()}:{os.getgid()}",
                    "-e",
                    "HOME=/tmp/dotfiles-test-home",
                    "-v",
                    f"{repo_root}:/workspace:ro",
                    IMAGE_NAME,
                ]
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(run_smoke_test(Path(__file__).resolve().parents[2]))
