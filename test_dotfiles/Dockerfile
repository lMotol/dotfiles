FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    bash \
    build-essential \
    ca-certificates \
    curl \
    fd-find \
    file \
    git \
    locales \
    neovim \
    npm \
    ripgrep \
    sudo \
    tmux \
    universal-ctags \
    unzip \
    xz-utils \
    zsh && \
    locale-gen en_US.UTF-8

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

RUN useradd -m -s /bin/bash tester && \
    printf 'tester ALL=(ALL) NOPASSWD:ALL\n' >/etc/sudoers.d/tester && \
    chmod 0440 /etc/sudoers.d/tester && \
    install -d -o tester -g tester /workspace

COPY entrypoint.sh /usr/local/bin/test-dotfiles-entrypoint
COPY verify_setup.sh /usr/local/bin/verify-dotfiles-setup

RUN chmod +x /usr/local/bin/test-dotfiles-entrypoint /usr/local/bin/verify-dotfiles-setup

USER tester
WORKDIR /workspace

ENTRYPOINT ["/usr/local/bin/test-dotfiles-entrypoint"]
