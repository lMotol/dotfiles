#!/bin/bash -e

# 必要なツールをインストール (Mac 用)
if ! command -v brew &>/dev/null; then
	echo "Homebrewがインストールされていません。インストールします。"
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 必要なツールをインストール
brew install curl git ripgrep tmux fd

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

# nvim のインストール
if command -v nvim >/dev/null 2>&1; then
	echo "Neovim は既にインストールされています。"
else
	echo "Neovim をインストールします。"
	brew install neovim
	which nvim
	nvim --version
fi

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
