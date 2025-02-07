# nvim のインストール
arch=$(uname -m)

echo "Detected architecture: $arch"

# アーキテクチャに応じた条件分岐
if [[ "$arch" == "x86_64" || "$arch" == "i386" || "$arch" == "i686" ]]; then
    echo "x86 アーキテクチャが検出されました。"
    # x86 向けの処理をここに記述
elif [[ "$arch" == "aarch64" || "$arch" == "armv7l" ]]; then
    echo "ARM アーキテクチャが検出されました。"
    # ARM 向けの処理をここに記述
else
    echo "不明なアーキテクチャ: $arch"
    # その他のアーキテクチャへの対応処理を記述
fi
if command -v nvim >/dev/null 2>&1; then
    echo "Neovim は既にインストールされています。"
else
    cd
    if [[ "$arch" == "x86_64" || "$arch" == "i386" || "$arch" == "i686" ]]; then
        curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.appimage
        chmod u+x nvim-linux-x86_64.appimage
        ./nvim-linux-x86_64.appimage --appimage-extract
    elif [[ "$arch" == "aarch64" || "$arch" == "armv7l" ]]; then
        curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-arm64.appimage
        chmod u+x nvim-linux-arm64.appimage
        ./nvim-linux-arm64.appimage --appimage-extract
    fi
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
