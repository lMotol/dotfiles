#!/usr/bin/env bash

set -euo pipefail

WORKSPACE_DIR="${WORKSPACE_DIR:-/workspace}"
REPO_DIR="$(mktemp -d /tmp/dotfiles-linux-test.XXXXXX)"
FAKE_BIN_DIR="$HOME/.local/bin"
VERIFY_SCRIPT=""

cleanup() {
    rm -rf "$REPO_DIR"
}

trap cleanup EXIT

mkdir -p "$FAKE_BIN_DIR"

cat <<'EOF' >"$FAKE_BIN_DIR/codex"
#!/usr/bin/env bash
if [ "${1:-}" = "--version" ]; then
    printf 'codex test stub\n'
    exit 0
fi
printf 'codex test stub\n'
EOF

cat <<'EOF' >"$FAKE_BIN_DIR/lazygit"
#!/usr/bin/env bash
if [ "${1:-}" = "--version" ]; then
    printf 'lazygit test stub\n'
    exit 0
fi
printf 'lazygit test stub\n'
EOF

chmod +x "$FAKE_BIN_DIR/codex" "$FAKE_BIN_DIR/lazygit"

cp -a "$WORKSPACE_DIR/." "$REPO_DIR/"

VERIFY_SCRIPT="$REPO_DIR/test_dotfiles/verify_setup.sh"

export PATH="$FAKE_BIN_DIR:$PATH"
export CI=true
export SETUP_SKIP_SYSTEM_PACKAGES=1
export SETUP_STRICT_INSTALL_SCRIPTS=1
unset EDITOR VISUAL GIT_EDITOR FCEDIT NVM_DIR

bash -n "$REPO_DIR/setup"

"$REPO_DIR/setup"

"$REPO_DIR/setup"

if command -v verify-dotfiles-setup >/dev/null 2>&1; then
    verify-dotfiles-setup "$REPO_DIR"
else
    bash "$VERIFY_SCRIPT" "$REPO_DIR"
fi

printf 'Setup smoke test completed successfully.\n'
