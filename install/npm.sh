#!/bin/bash

set -euo pipefail

# npm のインストール（nvm経由）

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

# shellcheck source=/dev/null
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

if command -v npm &>/dev/null; then
    echo "npm is already installed (version: $(npm -v))"
    exit 0
fi

echo "npm is not installed. Installing via nvm..."

# nvmのインストール
if ! command -v nvm &>/dev/null; then
    echo "Installing nvm..."
    PROFILE=/dev/null curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

    # shellcheck source=/dev/null
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

    echo "nvm has been installed."
fi

if ! command -v nvm &>/dev/null; then
    echo "Error: nvm is not available after installation"
    exit 1
fi

# Node.js と npm のインストール
echo "Installing Node.js LTS via nvm..."
nvm install --lts
nvm alias default 'lts/*'
nvm use --lts

echo "npm has been installed successfully!"
npm -v
