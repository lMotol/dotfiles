#!/bin/bash -e

# Poetry インストールスクリプト

if command -v poetry &>/dev/null; then
    echo "Poetry is already installed ($(poetry --version))"
    exit 0
fi

echo "Installing Poetry..."
curl -sSL https://install.python-poetry.org | python3 -

# シェル設定ファイルの判定
CURRENT_SHELL=$(basename "$SHELL")
case "$CURRENT_SHELL" in
    bash)
        TARGET_RC="$HOME/.bashrc"
        ;;
    zsh)
        TARGET_RC="$HOME/.zshrc"
        ;;
    *)
        echo "Unsupported shell: $CURRENT_SHELL"
        TARGET_RC="$HOME/.profile"
        ;;
esac

EXPORT_LINE='export PATH="$HOME/.local/bin:$PATH"'

if [ ! -f "$TARGET_RC" ]; then
    touch "$TARGET_RC"
fi

if ! grep -Fq "$HOME/.local/bin" "$TARGET_RC"; then
    echo "" >> "$TARGET_RC"
    echo "# Poetry" >> "$TARGET_RC"
    echo "$EXPORT_LINE" >> "$TARGET_RC"
    echo "Added Poetry to PATH in $TARGET_RC"
else
    echo "Poetry PATH already configured in $TARGET_RC"
fi

echo "Poetry installation complete!"
echo "Please reload your shell or run: source $TARGET_RC"
