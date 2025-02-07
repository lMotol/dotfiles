#!/bin/bash
set -e

# クローン先ディレクトリ
DOTFILES_DIR="$HOME/dotfiles"

# dotfiles リポジトリの URL（適宜ご自身のリポジトリに変更してください）
REPO_URL="https://github.com/lMotol/dotfiles.git"

# リポジトリが既に存在していなければクローン
if [ ! -d "$DOTFILES_DIR/.git" ]; then
    echo "Cloning dotfiles repository..."
    git clone "$REPO_URL" "$DOTFILES_DIR"
else
    echo "Dotfiles repository already exists. Pulling latest changes..."
    cd "$DOTFILES_DIR" && git pull
fi

cd $DOTFILES_DIR

# dotfiles 内にセットアップスクリプト（例: setup.sh）がある場合は実行
if [ -f "install.sh" ]; then
    echo "Running setup script..."
    bash "install.sh"
else
    echo "No setup script found in the dotfiles repository."
fi

# 必要に応じてシェルを起動（または、他のコマンドを実行）
exec bash
