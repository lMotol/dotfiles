FROM ubuntu:latest

# 非対話的なインストールのための環境変数
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    zsh \
    sudo \
    locales && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

# ロケールの設定
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

# 任意ですが、作業用ユーザーを作成（root 以外で作業したい場合）
RUN useradd -ms /bin/bash devuser && \
    echo "devuser:devuser" | chpasswd && \
    adduser devuser sudo

# 作業ディレクトリの設定
WORKDIR /home/devuser

# entrypoint スクリプトをコンテナ内にコピー
COPY entrypoint.sh /home/devuser/entrypoint.sh
RUN sudo chmod +x /home/devuser/entrypoint.sh

# 作業ユーザーに切り替え
USER devuser

# デフォルトのコマンドは entrypoint スクリプトの実行
CMD ["/home/devuser/entrypoint.sh"]

# コンテナ起動時のデフォルトコマンド
CMD [ "bash" ]
