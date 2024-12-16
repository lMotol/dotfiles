#!/bin/bash -e

# 必要なツールをインストール
sudo apt-get install -y curl git ripgrep build-essential tmux fd-find unzip

# tmux plugin manager のインストール
TARGET_DIR="$HOME/.tmux/plugins/tpm"
if [ -d "$TARGET_DIR" ]; then
    if [ -d "$TARGET_DIR/.git" ]; then
        cd "$TARGET_DIR"
        git pull origin master
    else
        exit 1
    fi
else
    mkdir -p $TARGET_DIR
    git clone https://github.com/tmux-plugins/tpm $TARGET_DIR
fi
~/.tmux/plugins/tpm/tpm

# nvim のインストール
if command -v nvim >/dev/null 2>&1; then
    echo "Neovim は既にインストールされています。"
else
    cd
    curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage
    chmod u+x nvim.appimage
    ./nvim.appimage --appimage-extract
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

# npm のインストール
# npm がインストールされているか確認
if command -v npm &>/dev/null; then
    echo "npm is already installed (version: $(npm -v))"
else
    echo "npm is not installed. Installing..."

    # nvm がインストールされているか確認
    if command -v nvm &>/dev/null; then
        echo "Using nvm to install Node.js and npm..."
        nvm install --lts
    else
        # nvm がインストールされていない場合、nvm をインストール
        echo "nvm is not installed. Installing nvm..."

        # nvm インストールスクリプトを実行
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

        # nvm のインストールが完了した後、シェルを再読み込み
        echo "nvm has been installed. Please restart your terminal or run 'source ~/.bashrc' (or source ~/.zshrc if you use zsh)."

        # インストール後、nvm を使って Node.js と npm をインストール
        echo "Using nvm to install Node.js and npm..."
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
        nvm install --lts
    fi

    echo "npm has been installed. Verifying installation..."
    npm -v
fi

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
# for dotfile in .??*; do
cd ~/dotfiles
find . -maxdepth 1 -name ".*" ! -name "." ! -name ".." | while read -r dotfile; do
    # 無視するファイルをスキップ
    basename_dotfile=$(basename "$dotfile")
    [[ $basename_dotfile =~ $IGNORE_PATTERN ]] && continue

    echo "$dotfile"

    # ディレクトリ構造を維持しながらリンクを作成
    if [[ $dotfile == ".config" ]]; then
        echo "dsvdssdvf"
        for subdir in "$dotfile"/*; do
            link_dotfiles "$(pwd)/$subdir" "$HOME/$dotfile/$(basename "$subdir")"
        done
    else
        # 通常のドットファイルやディレクトリはそのままリンク
        link_dotfiles "$(pwd)/$dotfile" "$HOME/$dotfile"
    fi
done

echo "Success"
