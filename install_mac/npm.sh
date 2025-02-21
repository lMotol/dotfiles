# npm のインストール
if command -v npm &>/dev/null; then
    echo "npm is already installed (version: $(npm -v))"
else
    echo "npm is not installed. Installing..."
    if command -v nvm &>/dev/null; then
        echo "Using nvm to install Node.js and npm..."
        nvm install --lts
    else
        echo "nvm is not installed. Installing nvm..."
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
        echo "nvm has been installed. Please restart your terminal or run 'source ~/.bashrc' (or source ~/.zshrc if you use zsh)."
        echo "Using zsh: source ~/.zshrc"
        source ~/.zshrc
        echo "Using nvm to install Node.js and npm..."
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
        nvm install --lts
    fi

    echo "npm has been installed. Verifying installation..."
    npm -v
fi
