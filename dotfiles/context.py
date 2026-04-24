from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Application settings and runtime context.

    This uses Pydantic's BaseSettings so values can be provided via environment
    variables and validated automatically. It's intentionally small and mirrors
    the previous AppContext shape.
    """

    root: Path
    home: Path = Field(default_factory=lambda: Path("~").expanduser().resolve())
    os_name: Optional[str] = None
    arch: Optional[str] = None
    ci: bool = Field(False, env=("CI", "GITHUB_ACTIONS"))
    skip_system_packages: bool = Field(False, env=("SKIP_SYSTEM_PACKAGES", "SETUP_SKIP_SYSTEM_PACKAGES"))
    strict_install_scripts: bool = Field(False, env=("STRICT_INSTALL_SCRIPTS", "SETUP_STRICT_INSTALL_SCRIPTS"))

    class Config:
        env_prefix = ""
        arbitrary_types_allowed = True

    @validator("os_name", pre=True, always=True)
    def _detect_os(cls, v):
        if v:
            return v
        try:
            platform = __import__("os").uname().sysname
        except Exception:
            return "unknown"
        if platform == "Darwin":
            return "macos"
        if platform == "Linux":
            return "linux"
        return "unknown"

    @validator("arch", pre=True, always=True)
    def _detect_arch(cls, v):
        if v:
            return v
        try:
            return __import__("os").uname().machine
        except Exception:
            return "unknown"

    @validator("ci", pre=True, always=True)
    def _detect_ci(cls, v):
        if v:
            return True
        env = __import__("os").environ
        ci_val = env.get("CI") or env.get("GITHUB_ACTIONS")
        if isinstance(ci_val, str) and ci_val.lower() in {"1", "true", "yes"}:
            return True
        return False


def build_settings_from_args(args: object, root: Path) -> Settings:
    """Create Settings from CLI args and environment.

    This keeps the CLI surface small: Typer will populate an object with the
    same attributes we used before and this function folds them into Pydantic.
    """
    # pick values from args if present, otherwise let Settings detect from env
    data = {"root": root}
    for key in ("home", "os_name", "arch", "ci", "skip_system_packages", "strict_install_scripts"):
        if hasattr(args, key):
            val = getattr(args, key)
            if isinstance(val, bool):
                if val:
                    data[key] = val
            elif val is not None:
                data[key] = val
    return Settings(**data)
