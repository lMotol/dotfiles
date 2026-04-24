# dotfiles

個人的なdotfilesリポジトリです。Neovim、tmux、シェル設定などを管理しています。

![Test Status](https://github.com/lMotol/dotfiles/actions/workflows/test.yml/badge.svg)

## 構成

```
.
├── .clang-format          # C/C++ フォーマット設定
├── .gitconfig             # Git 設定
├── .tmux.conf             # tmux 設定
├── .config/
│   ├── nvim/              # Neovim 設定
│   ├── sheldon/           # Sheldon（zshプラグインマネージャー）設定
│   └── shell/             # shell 共通設定
├── ast_grep/              # ast-grep 設定
├── install/               # インストールスクリプト
├── test_dotfiles/         # Linux 用 smoke test
├── setup                  # メインセットアップスクリプト
└── poetry_install.sh      # Poetry インストールスクリプト
```

## セットアップ

### 前提条件

- Git
- Bash/Zsh
- curl

### インストール手順

1. このリポジトリをクローン:

```bash
git clone --recursive https://github.com/lMotol/dotfiles.git ~/src/dotfiles
cd ~/src/dotfiles
```

2. セットアップスクリプトを実行:

```bash
./setup
```

セットアップスクリプトは以下を実行します:
- OSを自動検出（Linux/macOS）
- 必要なパッケージのインストール
- 追加ツールのインストール（fzf, Neovim, npm, tpm）
- dotfilesのシンボリックリンク作成
- `~/.bashrc`, `~/.bash_profile`, `~/.zshrc` に managed block を追加

3. シェルを再読み込み:

```bash
exec $SHELL -l
```

4. tmuxプラグインをインストール:

```bash
tmux
# tmux内で: prefix + I
```

## サポートOS

- **Linux**: Ubuntu/Debian系（apt使用）
- **macOS**: Homebrew使用

## インストールされるツール

### 共通
- Git
- Ripgrep
- Tmux
- Neovim
- Universal Ctags
- fzf
- Node.js/npm (via nvm)
- TPM (Tmux Plugin Manager)

### Linux固有
- build-essential
- fd-find
- unzip

### macOS固有
- Homebrew（未インストールの場合）
- fd
- Sheldon

## オプション: Poetry

Pythonのパッケージマネージャー Poetryをインストールする場合:

```bash
./poetry_install.sh
```

## テスト

### GitHub Actions

このリポジトリはGitHub Actionsで自動テストされています。プッシュやプルリクエスト時に以下がテストされます：

- **Linux Docker**: `setup` の smoke test
- **macOS runner**: path-independent な `setup` の smoke test
- **ShellCheck**: 全スクリプトの静的解析

### ローカルテスト

Linux smoke test を Docker で実行できます:

```bash
docker build -t dotfiles-linux-test -f test_dotfiles/Dockerfile test_dotfiles
docker run --rm -v "$(pwd):/workspace:ro" dotfiles-linux-test
```

## カスタマイズ

各設定ファイルを直接編集してカスタマイズしてください:
- Neovim: `.config/nvim/`
- tmux: `.tmux.conf`
- Shell: `.config/shell/`

## トラブルシューティング

### シンボリックリンクが作成されない

```bash
cd /path/to/dotfiles
./setup
```

### tmuxプラグインがインストールされない

tmux内で `prefix + I` を押してください（デフォルトのprefixは `Ctrl+b`）。

## ライセンス

MIT
