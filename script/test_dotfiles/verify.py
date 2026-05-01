from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def _assert_exists(path: Path) -> None:
    if not path.exists():
        raise RuntimeError(f"Missing expected path: {path}")


def _assert_dir(path: Path) -> None:
    if not path.is_dir():
        raise RuntimeError(f"Missing expected directory: {path}")


def _assert_symlink_target(path: Path, expected: Path) -> None:
    if not path.is_symlink():
        raise RuntimeError(f"Expected symlink: {path}")
    actual = os.readlink(path)
    if actual != str(expected):
        raise RuntimeError(
            f"Unexpected symlink target for {path}\nexpected: {expected}\nactual:   {actual}"
        )


def _assert_contains(path: Path, expected: str) -> None:
    if expected not in path.read_text():
        raise RuntimeError(f"Expected {path} to contain: {expected}")


def _assert_count(path: Path, pattern: str, expected_count: int) -> None:
    actual_count = path.read_text().count(pattern)
    if actual_count != expected_count:
        raise RuntimeError(
            f"Unexpected match count for {pattern} in {path}\nexpected: {expected_count}\nactual:   {actual_count}"
        )


def _assert_command_output(expected: str, command: list[str]) -> None:
    actual = subprocess.run(command, check=True, text=True, capture_output=True).stdout.strip()
    if actual != expected:
        raise RuntimeError(f"Unexpected command output\nexpected: {expected}\nactual:   {actual}")


def _assert_command_output_contains(expected: str, command: list[str]) -> None:
    actual = subprocess.run(command, check=True, text=True, capture_output=True).stdout.strip()
    if expected not in actual:
        raise RuntimeError(f"Unexpected command output\nexpected to contain: {expected}\nactual:              {actual}")


def _assert_editor_environment() -> None:
    actual = subprocess.run(
        ["bash", "-lc", 'printf "%s|%s|%s|%s|%s" "$EDITOR" "$VISUAL" "$GIT_EDITOR" "$FCEDIT" "$NVM_DIR"'],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    editor, visual, git_editor, fcedit, nvm_dir = actual.split("|", maxsplit=4)
    if (editor, visual, git_editor, fcedit) != ("nvim", "nvim", "nvim", "nvim"):
        raise RuntimeError(f"Unexpected editor environment: {actual}")
    if not nvm_dir.endswith("/.nvm"):
        raise RuntimeError(f"Unexpected NVM_DIR: {nvm_dir}")


def verify_setup(home: Path, repo_dir: Path) -> None:
    home = home.resolve()

    _assert_exists(home / ".bashrc")
    _assert_exists(home / ".bash_profile")
    _assert_exists(home / ".zshrc")
    _assert_dir(home / ".config")
    _assert_dir(home / ".config/shell")
    _assert_dir(home / ".tmux/plugins/tpm")
    _assert_dir(home / ".fzf")

    _assert_symlink_target(home / ".tmux.conf", repo_dir / ".tmux.conf")
    _assert_symlink_target(home / ".config/shell/env.sh", repo_dir / ".config/shell/env.sh")
    _assert_symlink_target(home / ".config/shell/bashrc", repo_dir / ".config/shell/bashrc")
    _assert_symlink_target(home / ".config/shell/zshrc", repo_dir / ".config/shell/zshrc")

    _assert_contains(home / ".bashrc", '# >>> dotfiles bashrc >>>')
    _assert_contains(home / ".bashrc", f'[ -f "{home}/.config/shell/bashrc" ] && . "{home}/.config/shell/bashrc"')
    _assert_contains(home / ".bash_profile", '# >>> dotfiles bash login >>>')
    _assert_contains(home / ".bash_profile", f'[ -f "{home}/.bashrc" ] && . "{home}/.bashrc"')
    _assert_contains(home / ".zshrc", '# >>> dotfiles zshrc >>>')
    _assert_contains(home / ".zshrc", f'[ -f "{home}/.config/shell/zshrc" ] && . "{home}/.config/shell/zshrc"')

    _assert_count(home / ".bashrc", '# >>> dotfiles bashrc >>>', 1)
    _assert_count(home / ".bash_profile", '# >>> dotfiles bash login >>>', 1)
    _assert_count(home / ".zshrc", '# >>> dotfiles zshrc >>>', 1)

    _assert_editor_environment()
    _assert_command_output_contains("tree-sitter", ["bash", "-ic", "tree-sitter --version"])

    _assert_contains(home / ".config/shell/zshrc", "bindkey '^X^E' edit-command-line")
    if shutil.which("zsh"):
        _assert_command_output('"^X^E" edit-command-line', ["zsh", "-ic", 'bindkey "^X^E"'])

    print(f"Verified setup outputs in {home}")
