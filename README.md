# dotfiles

個人的なdotfilesリポジトリです。Neovim、tmux、シェル設定などを管理しています。

## 構成

```
.
├── .clang-format          # C/C++ フォーマット設定
├── .tmux.conf             # tmux 設定
├── .config/
│   ├── nvim/              # Neovim 設定
│   └── sheldon/           # Sheldon（zshプラグインマネージャー）設定
├── ast_grep/              # ast-grep 設定
├── install/               # インストールスクリプト
├── test_dotfiles/         # Docker テスト環境
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
git clone --recursive https://github.com/yourusername/dotfiles.git ~/dotfiles
cd ~/dotfiles
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

Docker環境でセットアップをテストできます:

```bash
cd test_dotfiles
docker compose up
```

## カスタマイズ

各設定ファイルを直接編集してカスタマイズしてください:
- Neovim: `.config/nvim/`
- tmux: `.tmux.conf`
- Shell: ホームディレクトリの`.bashrc`または`.zshrc`

## トラブルシューティング

### シンボリックリンクが作成されない

```bash
cd ~/dotfiles
./setup
```

### tmuxプラグインがインストールされない

tmux内で `prefix + I` を押してください（デフォルトのprefixは `Ctrl+b`）。

## ライセンス

MIT
