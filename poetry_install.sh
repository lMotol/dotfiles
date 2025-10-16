#!/bin/bash
# Poetry インストールスクリプト

set -e

# ユーティリティ関数を読み込み
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=install/detect_os.sh
source "$SCRIPT_DIR/install/detect_os.sh"

# 既にインストールされているかチェック
if has_command poetry; then
    echo "Poetry is already installed ($(poetry --version))"
    exit 0
fi

echo "Installing Poetry..."
curl -sSL https://install.python-poetry.org | python3 -

# PATHに追加
OS="$(detect_os)"
add_to_path "$HOME/.local/bin" "Poetry" "$OS"

echo "✓ Poetry installation complete!"
echo "Please reload your shell or run: source $(get_shell_rc "$OS")"
