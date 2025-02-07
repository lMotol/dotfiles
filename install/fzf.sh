# fzf のインストール
rm -r ~/.fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
CURRENT_SHELL=$(basename "$SHELL")
if [ "$CURRENT_SHELL" = "bash" ]; then
    CONFIG_FILE="$HOME/.bashrc"
    ADD_LINE='eval "$(fzf --bash)"'
elif [ "$CURRENT_SHELL" = "zsh" ]; then
    CONFIG_FILE="$HOME/.zshrc"
    ADD_LINE='source <(fzf --zsh)'
else
    echo "サポートされていないシェルです: $CURRENT_SHELL"
    exit 1
fi
grep -qxF "$ADD_LINE" "$CONFIG_FILE" || echo "$ADD_LINE" >>"$CONFIG_FILE"
