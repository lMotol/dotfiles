# nvim のインストール
if command -v nvim >/dev/null 2>&1; then
    echo "Neovim は既にインストールされています。"
else
    cd
    curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.appimage
    chmod u+x nvim-linux-x86_64.appimage
    nvim-linux-x86_64.appimage --appimage-extract
    ./squashfs-root/AppRun --version
    if [ -d "/squashfs-root" ]; then
        sudo rm -r /squashfs-root
    fi
    sudo mv squashfs-root /
    if [ -d "/usr/bin/nvim" ]; then
        sudo rm -r /usr/bin/nvim
    fi
    sudo ln -s /squashfs-root/AppRun /usr/bin/nvim
    which nvim
    nvim --version
fi
