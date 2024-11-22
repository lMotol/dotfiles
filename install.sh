#!/bin/bash -e

# 必要なツールをインストール
sudo apt-get install -y curl git ripgrep tmux

# tmux plugin manager のインストール
TARGET_DIR="~/.tmux/plugins/tpm"
if [ -d "$TARGET_DIR" ]; then
    if [ -d "$TARGET_DIR/.git" ]; then
        cd "$TARGET_DIR"
        git pull origin master
    else
        exit 1
    fi
else
    git clone https://github.com/tmux-plugins/tpm $TARGET_DIR
fi

tmux &
~/.tmux/plugins/tpm/bin/install_plugins
tmux kill-server

# nvim のインストール
cd
curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage
chmod u+x nvim.appimage
./nvim.appimage --appimage-extract
./squashfs-root/AppRun --version
sudo mv squashfs-root /
sudo ln -s /squashfs-root/AppRun /usr/bin/nvim
which nvim
nvim --version

# 無視するパターンを定義
IGNORE_PATTERN="^\.(git|travis)"

# シンボリックリンクを作成する関数
link_dotfiles() {
    local src=$1
    local dest=$2

    # ディレクトリの場合、再帰的にリンクを作成
    if [[ -d $src ]]; then
        mkdir -p "$dest" # 必要ならディレクトリを作成
        for file in "$src"/*; do
            link_dotfiles "$file" "$dest/$(basename "$file")"
        done
    else
        ln -snfv "$src" "$dest"
    fi
}

echo "Creating dotfile links..."

# カレントディレクトリ内のドットファイルを処理
for dotfile in .??*; do
    # 無視するファイルをスキップ
    [[ $dotfile =~ $IGNORE_PATTERN ]] && continue

    # ディレクトリ構造を維持しながらリンクを作成
    link_dotfiles "$(pwd)/$dotfile" "$HOME/$dotfile"
done

echo "Success"
