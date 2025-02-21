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
# tmuxを自動で起動して、tpmをインストールする部分はマニュアルで行うべきです
echo "tmux を起動し、tpm をインストールしてください。"
echo "tmux を起動するには 'tmux' と入力してください。"
echo "tpm をインストールするには tmux 内で 'prefix + I' を押してください。"
