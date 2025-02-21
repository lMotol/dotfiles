#!/bin/bash
set -e

# クローン先ディレクトリ
DOTFILES_DIR="$HOME/dotfiles"
BRANCH_NAME="update-script"
COMMIT_HASH=43e1805b78cf14d755b3584a6ee2b7e62ea41279

REPO_URL="https://github.com/lMotol/dotfiles.git"

# リポジトリが既に存在していなければクローン
if [ ! -d "$DOTFILES_DIR/.git" ]; then
    echo "Cloning dotfiles repository..."
    git clone "$REPO_URL" "$DOTFILES_DIR" -b $BRANCH_NAME
else
    echo "Dotfiles repository already exists. Pulling latest changes..."
    cd "$DOTFILES_DIR" && git pull
fi

cd $DOTFILES_DIR
