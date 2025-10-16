#!/bin/bash
# tmux plugin manager のインストール

TARGET_DIR="$HOME/.tmux/plugins/tpm"

if [ -d "$TARGET_DIR" ]; then
    if [ -d "$TARGET_DIR/.git" ]; then
        echo "Updating tpm..."
        cd "$TARGET_DIR"
        git pull origin master
    else
        echo "Error: $TARGET_DIR exists but is not a git repository"
        exit 1
    fi
else
    echo "Installing tpm..."
    mkdir -p "$TARGET_DIR"
    git clone https://github.com/tmux-plugins/tpm "$TARGET_DIR"
fi

echo "tpm installation complete!"
echo "To install tmux plugins:"
echo "  1. Start tmux: tmux"
echo "  2. Press: prefix + I (capital i)"
