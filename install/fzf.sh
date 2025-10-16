#!/bin/bash
# fzf のインストール

FZF_DIR="$HOME/.fzf"

if [ -d "$FZF_DIR" ]; then
    echo "fzf directory exists. Removing and reinstalling..."
    rm -rf "$FZF_DIR"
fi

echo "Installing fzf..."
git clone --depth 1 https://github.com/junegunn/fzf.git "$FZF_DIR"
"$FZF_DIR/install" --all

echo "fzf installation complete!"
