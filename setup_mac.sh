#!/bin/bash -e

# パッケージ管理ツールのインストール
if ! command -v brew &>/dev/null; then
    echo "--Homebrew install--"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# brew によるインストール
brew install curl git ripgrep tmux fd neovim sheldon direnv

# brew 非対応ツールのインストール
INSTALL_DIR="install_mac"
# install script を実行
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: $INSTALL_DIR directory does not exist."
    exit 1
fi
for script in "$INSTALL_DIR"/*; do
    if [ -f "$script" ]; then
        echo "exec: $script"
        if [ -x "$script" ]; then
            "$script"
        else
            bash "$script"
        fi
    fi
done

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
        for subdir in "$dotfile"/*; do
            link_dotfiles "$(pwd)/$subdir" "$HOME/$dotfile/$(basename "$subdir")"
        done
    else
        # 通常のドットファイルやディレクトリはそのままリンク
        link_dotfiles "$(pwd)/$dotfile" "$HOME/$dotfile"
    fi
done

echo "Success"
