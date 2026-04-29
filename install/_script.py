from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def run_install_script(target: str) -> int:
    from cli import main

    return main(["install", target, *sys.argv[1:]])


def run_detect_os_script() -> int:
    from cli import main

    return main(["detect-os", *sys.argv[1:]])
