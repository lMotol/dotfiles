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
├── cli.py                 # setup CLI
├── context.py             # setup 実行コンテキスト
├── dotfiles_cli.py        # setup CLI entrypoint
├── installers.py          # installer registry
├── install/               # ツール別 installer 実装
├── setup_flow.py          # setup 本体フロー
├── util.py                # Python 実行ユーティリティ
├── test_dotfiles/         # Linux 用 smoke test
└── setup                  # uv venv を作って setup CLI を起動
```

## セットアップ

### 前提条件

- Git
- Bash/Zsh
- curl
- uv

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
- `uv venv .setup-venv` で setup 用の仮想環境を作成
- `uv pip install --editable .` で CLI 依存を `.setup-venv` に同期
- `.setup-venv` 内の Python で `dotfiles_cli.py setup` を実行
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

Python の仮想環境を作り直したい場合は、`.setup-venv/` を消してからもう一度 `./setup` を実行してください。

## テスト

### GitHub Actions

このリポジトリはGitHub Actionsで自動テストされています。プッシュやプルリクエスト時に以下がテストされます：

- **Linux Docker**: `setup` の smoke test
- **macOS runner**: path-independent な `setup` の smoke test
- **ShellCheck**: 全スクリプトの静的解析

### ローカルテスト

Linux smoke test は `test_dotfiles/run.sh` から実行します:

```bash
bash test_dotfiles/run.sh
```

このラッパーは Docker image を build して smoke test を実行し、ログを `test_dotfiles/logs/` に保存します。詳細は `test_dotfiles/README.md` を参照してください。

Poetry を追加で入れたい場合は、setup で作成された Python から CLI を直接使えます:

```bash
./.setup-venv/bin/python dotfiles_cli.py install poetry
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
