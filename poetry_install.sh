#!/bin/bash -e

curl -sSL https://install.python-poetry.org | python3 -

if grep -Fxq "$EXPORT_LINE" "$TARGET_RC"; then
    echo "$TARGET_RC に既に追記済みです。"
else
    EXPORT_LINE="export PATH=\"\$HOME/.local/share/pypoetry/venv/bin:\$PATH\""
    TARGET_RC="$HOME/.bashrc"
    echo "$EXPORT_LINE" >>"$TARGET_RC"
fi
