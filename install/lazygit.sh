#!/bin/bash

set -euo pipefail

# lazygit のインストール（Linux専用）

# macOSの場合はスキップ
if [[ "$(uname -s)" == "Darwin" ]]; then
    echo "macOS detected. lazygit should be installed via Homebrew."
    exit 0
fi

if command -v lazygit >/dev/null 2>&1; then
    echo "lazygit is already installed ($(lazygit --version | head -n 1))"
    exit 0
fi

tmp_dir=$(mktemp -d)

cleanup() {
    rm -rf "$tmp_dir"
}

trap cleanup EXIT

arch=$(uname -m)

LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | \grep -Po '"tag_name": *"v\K[^"]*')

case "$arch" in
    x86_64)
        lazygit_arch="x86_64"
        ;;
    aarch64|arm64)
        lazygit_arch="arm64"
        ;;
    *)
        echo "Unsupported architecture: $arch"
        exit 1
        ;;
esac

curl -fsSLo "$tmp_dir/lazygit.tar.gz" "https://github.com/jesseduffield/lazygit/releases/download/v${LAZYGIT_VERSION}/lazygit_${LAZYGIT_VERSION}_Linux_${lazygit_arch}.tar.gz"
tar -C "$tmp_dir" -xf "$tmp_dir/lazygit.tar.gz" lazygit
sudo install -m 0755 "$tmp_dir/lazygit" /usr/local/bin/lazygit

echo "lazygit installation complete!"
lazygit --version
