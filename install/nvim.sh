#!/bin/bash

set -euo pipefail

# Neovim のインストール（Linux専用）

# macOSの場合はスキップ
if [[ "$(uname -s)" == "Darwin" ]]; then
    echo "macOS detected. Neovim should be installed via Homebrew."
    exit 0
fi

if command -v nvim >/dev/null 2>&1; then
    echo "Neovim is already installed ($(nvim --version | head -n1))"
    exit 0
fi

arch=$(uname -m)
tmp_dir=$(mktemp -d)

cleanup() {
    rm -rf "$tmp_dir"
}

trap cleanup EXIT

echo "Detected architecture: $arch"

install_root="/opt/nvim"
binary_path="/usr/local/bin/nvim"

case "$arch" in
    x86_64|i386|i686)
        echo "Installing Neovim for x86_64..."
        appimage_url="https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.appimage"
        ;;
    aarch64|armv7l|arm64)
        echo "Installing Neovim for ARM64..."
        appimage_url="https://github.com/neovim/neovim/releases/latest/download/nvim-linux-arm64.appimage"
        ;;
    *)
        echo "Unsupported architecture: $arch"
        exit 1
        ;;
esac

curl -fsSLo "$tmp_dir/nvim.appimage" "$appimage_url"
chmod u+x "$tmp_dir/nvim.appimage"

(
    cd "$tmp_dir"
    ./nvim.appimage --appimage-extract >/dev/null
)

sudo rm -rf "$install_root"
sudo mv "$tmp_dir/squashfs-root" "$install_root"
sudo ln -sf "$install_root/AppRun" "$binary_path"

echo "Neovim installation complete!"
nvim --version | head -n 1
