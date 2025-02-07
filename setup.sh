#!/bin/bash -e

sudo apt update
sudo apt upgrade
sudo apt-get install -y curl git ripgrep build-essential tmux fd-find unzip

INSTALL_DIR="install"
# install script を実行
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: $INSTALL_DIR ディレクトリが存在しません。"
    exit 1
fi
for script in "$INSTALL_DIR"/*; do
    if [ -f "$script" ]; then
        echo "実行中: $script"
        if [ -x "$script" ]; then
            "$script"
        else
            bash "$script"
        fi
    fi
done

# dotfiles のシンボリックリンクを作成
IGNORE_PATTERN="^\.(git|travis)"

link_dotfiles() {
    local src=$1
    local dest=$2
    if [ -d "$src" ]; then
        mkdir -p "$dest" # 必要ならディレクトリを作成
        for file in "$src"/*; do
            link_dotfiles "$file" "$dest/$(basename "$file")"
        done
    else
        ln -snfv "$src" "$dest"
    fi
}

echo "Creating dotfile links..."

cd ~/dotfiles
find . -maxdepth 1 -name ".*" ! -name "." ! -name ".." | while read -r dotfile; do
    basename_dotfile=$(basename "$dotfile")
    [[ $basename_dotfile =~ $IGNORE_PATTERN ]] && continue

    echo "$dotfile"
    if [[ $dotfile == ".config" ]]; then
        echo "dsvdssdvf"
        for subdir in "$dotfile"/*; do
            link_dotfiles "$(pwd)/$subdir" "$HOME/$dotfile/$(basename "$subdir")"
        done
    else
        link_dotfiles "$(pwd)/$dotfile" "$HOME/$dotfile"
    fi
done

echo "Success"
echo "シェルの設定ファイルが変更された場合はシェルの再読み込みを行うこと"
echo "tmux の設定を読み込むために tmux を起動し prefox + I を入力すること"
