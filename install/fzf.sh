#!/bin/bash

set -euo pipefail

# fzf のインストール

FZF_DIR="$HOME/.fzf"

if [ -d "$FZF_DIR" ]; then
    if [ -d "$FZF_DIR/.git" ]; then
        echo "Updating fzf..."
        git -C "$FZF_DIR" pull --ff-only
    else
        echo "Error: $FZF_DIR exists but is not a git repository"
        exit 1
    fi
else
    echo "Installing fzf..."
    git clone --depth 1 https://github.com/junegunn/fzf.git "$FZF_DIR"
fi

"$FZF_DIR/install" --all --no-update-rc

echo "fzf installation complete!"
