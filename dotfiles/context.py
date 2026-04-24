from __future__ import annotations

import os
from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path


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


@dataclass(frozen=True)
class AppContext:
    root: Path
    home: Path
    os_name: str
    arch: str
    ci: bool
    skip_system_packages: bool
    strict_install_scripts: bool

    @classmethod
    def from_args(cls, args: Namespace, root: Path) -> "AppContext":
        home = Path(os.environ.get("HOME", str(Path.home()))).expanduser().resolve()
        os_name = getattr(args, "os_name", None) or detect_os_name()
        ci = getattr(args, "ci", False) or in_ci()
        skip_system_packages = getattr(args, "skip_system_packages", False) or truthy(
            os.environ.get("SETUP_SKIP_SYSTEM_PACKAGES")
        )
        strict_install_scripts = getattr(args, "strict_install_scripts", False) or truthy(
            os.environ.get("SETUP_STRICT_INSTALL_SCRIPTS")
        )

        return cls(
            root=root,
            home=home,
            os_name=os_name,
            arch=detect_arch(),
            ci=ci,
            skip_system_packages=skip_system_packages,
            strict_install_scripts=strict_install_scripts,
        )
