#!/bin/bash
# npm のインストール（nvm経由）

if command -v npm &>/dev/null; then
    echo "npm is already installed (version: $(npm -v))"
    exit 0
fi

echo "npm is not installed. Installing via nvm..."

# nvmのインストール
if ! command -v nvm &>/dev/null; then
    echo "Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    
    # nvmを現在のシェルセッションで利用可能にする
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    
    echo "nvm has been installed."
fi

# Node.js と npm のインストール
echo "Installing Node.js LTS via nvm..."
nvm install --lts
nvm use --lts

echo "npm has been installed successfully!"
npm -v
