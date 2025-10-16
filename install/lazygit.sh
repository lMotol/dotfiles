#!/bin/bash
# Neovim のインストール（Linux専用）

# macOSの場合はスキップ
if [[ "$(uname -s)" == "Darwin" ]]; then
    echo "macOS detected. lazygit should be installed via Homebrew."
    exit 0
fi

if command -v lazygit >/dev/null 2>&1; then
    echo "lazygit is already installed ($(nvim --version | head -n1))"
    exit 0
fi

cd "$HOME" || exit 1

LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | \grep -Po '"tag_name": *"v\K[^"]*')
curl -Lo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/download/v${LAZYGIT_VERSION}/lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz"
tar xf lazygit.tar.gz lazygit
sudo install lazygit -D -t /usr/local/bin/

echo "lazygit installation complete!"
lazygit --version
