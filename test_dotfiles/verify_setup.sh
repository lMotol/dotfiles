#!/usr/bin/env bash

set -euo pipefail

REPO_DIR=${1:-}

if [ -z "$REPO_DIR" ]; then
    printf 'usage: %s <repo-dir>\n' "$0" >&2
    exit 1
fi

assert_exists() {
    if [ ! -e "$1" ]; then
        printf 'Missing expected path: %s\n' "$1" >&2
        exit 1
    fi
}

assert_dir() {
    if [ ! -d "$1" ]; then
        printf 'Missing expected directory: %s\n' "$1" >&2
        exit 1
    fi
}

assert_symlink_target() {
    local path=$1
    local expected=$2
    local actual

    if [ ! -L "$path" ]; then
        printf 'Expected symlink: %s\n' "$path" >&2
        exit 1
    fi

    actual=$(readlink "$path")
    if [ "$actual" != "$expected" ]; then
        printf 'Unexpected symlink target for %s\nexpected: %s\nactual:   %s\n' "$path" "$expected" "$actual" >&2
        exit 1
    fi
}

assert_contains() {
    local path=$1
    local expected=$2
    if ! grep -Fq "$expected" "$path"; then
        printf 'Expected %s to contain: %s\n' "$path" "$expected" >&2
        exit 1
    fi
}

assert_count() {
    local path=$1
    local pattern=$2
    local expected_count=$3
    local actual_count

    actual_count=$(grep -Fc "$pattern" "$path")
    if [ "$actual_count" -ne "$expected_count" ]; then
        printf 'Unexpected match count for %s in %s\nexpected: %s\nactual:   %s\n' "$pattern" "$path" "$expected_count" "$actual_count" >&2
        exit 1
    fi
}

assert_command_output() {
    local expected=$1
    shift
    local actual

    actual=$("$@")
    if [ "$actual" != "$expected" ]; then
        printf 'Unexpected command output\nexpected: %s\nactual:   %s\n' "$expected" "$actual" >&2
        exit 1
    fi
}

assert_exists "$HOME/.bashrc"
assert_exists "$HOME/.bash_profile"
assert_exists "$HOME/.zshrc"
assert_dir "$HOME/.config"
assert_dir "$HOME/.config/shell"
assert_dir "$HOME/.tmux/plugins/tpm"
assert_dir "$HOME/.fzf"

assert_symlink_target "$HOME/.tmux.conf" "$REPO_DIR/.tmux.conf"
assert_symlink_target "$HOME/.config/shell/env.sh" "$REPO_DIR/.config/shell/env.sh"
assert_symlink_target "$HOME/.config/shell/bashrc" "$REPO_DIR/.config/shell/bashrc"
assert_symlink_target "$HOME/.config/shell/zshrc" "$REPO_DIR/.config/shell/zshrc"

assert_contains "$HOME/.bashrc" '# >>> dotfiles bashrc >>>'
assert_contains "$HOME/.bashrc" "[ -f \"$HOME/.config/shell/bashrc\" ] && . \"$HOME/.config/shell/bashrc\""
assert_contains "$HOME/.bash_profile" '# >>> dotfiles bash login >>>'
assert_contains "$HOME/.bash_profile" "[ -f \"$HOME/.bashrc\" ] && . \"$HOME/.bashrc\""
assert_contains "$HOME/.zshrc" '# >>> dotfiles zshrc >>>'
assert_contains "$HOME/.zshrc" "[ -f \"$HOME/.config/shell/zshrc\" ] && . \"$HOME/.config/shell/zshrc\""

assert_count "$HOME/.bashrc" '# >>> dotfiles bashrc >>>' 1
assert_count "$HOME/.bash_profile" '# >>> dotfiles bash login >>>' 1
assert_count "$HOME/.zshrc" '# >>> dotfiles zshrc >>>' 1

assert_command_output \
    "nvim|nvim|nvim|nvim|$HOME/.nvm" \
    bash -lc 'printf "%s|%s|%s|%s|%s" "$EDITOR" "$VISUAL" "$GIT_EDITOR" "$FCEDIT" "$NVM_DIR"'

assert_contains "$HOME/.config/shell/zshrc" "bindkey '^X^E' edit-command-line"

if command -v zsh >/dev/null 2>&1; then
    assert_command_output "\"^X^E\" edit-command-line" zsh -ic 'bindkey "^X^E"'
fi

printf 'Verified setup outputs in %s\n' "$HOME"
