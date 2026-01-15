#!/bin/bash
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
echo "Detected architecture: $arch"

cd "$HOME" || exit 1

case "$arch" in
    x86_64|i386|i686)
        echo "Installing Neovim for x86_64..."
        curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.appimage
	chmod u+x nvim-linux-x86_64.appimage
	./nvim-linux-x86_64.appimage --appimage-extract
        rm nvim-linux-x86_64.appimage
	
        sudo rm -rf /squashfs-root
	sudo mv squashfs-root /
	sudo ln -s /squashfs-root/AppRun /usr/bin/nvim
        
        ;;
    aarch64|armv7l|arm64)
        echo "Installing Neovim for ARM64..."
        curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-arm64.appimage
        chmod u+x nvim-linux-arm64.appimage
        ./nvim-linux-arm64.appimage --appimage-extract
        
        sudo rm -rf /squashfs-root
        sudo mv squashfs-root /
        sudo ln -sf /squashfs-root/AppRun /usr/bin/nvim
        
        rm nvim-linux-arm64.appimage
        ;;
    *)
        echo "Unsupported architecture: $arch"
        exit 1
        ;;
esac

echo "Neovim installation complete!"
nvim --version
