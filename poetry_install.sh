#!/bin/bash -e

curl -sSL https://install.python-poetry.org | python3 -

CURRENT_SHELL=$(basename "$SHELL")

# 追加するPATH設定
ADD_PATH='export PATH="$HOME/.local/bin:$PATH"'

# 設定ファイルのパスを決定
if [ "$current_shell" = "bash" ]; then
    config_file="$HOME/.bashrc"
elif [ "$current_shell" = "zsh" ]; then
    config_file="$HOME/.zshrc"
else
    echo "現在使用しているシェルはbashでもzshでもありません。手動でPATHを追加してください。"
    exit 1
fi

# PATH設定が既に存在するか確認
if grep -Fxq "$path_export" "$config_file"; then
    echo "既に$path_exportが$config_fileに追加されています。"
else
    # PATH設定を設定ファイルに追加
    echo "$path_export" >>"$config_file"
    echo "$path_export を $config_file に追加しました。"
fi
