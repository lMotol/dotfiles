#!/bin/bash -e

sudo apt-get install curl git ripgrep neovim tmux

IGNORE_PATTERN="^\.(git|travis)"

echo "Create dotfile links."
for dotfile in .??*; do
	[[ $dotfile =~ $IGNORE_PATTERN ]] && continue
	ln -snfv "$(pwd)/$dotfile" "$HOME/$dotfile"
done
echo "Success"
