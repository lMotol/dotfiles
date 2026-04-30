FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    bash \
    ca-certificates \
    curl \
    file \
    locales \
    python3 \
    sudo \
    xz-utils \
    zsh && \
    locale-gen en_US.UTF-8

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    install -m 0755 /root/.local/bin/uv /usr/local/bin/uv

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

RUN useradd -m -s /bin/bash tester && \
    printf 'tester ALL=(ALL) NOPASSWD:ALL\n' >/etc/sudoers.d/tester && \
    chmod 0440 /etc/sudoers.d/tester && \
    install -d -o tester -g tester /workspace

COPY script/test_dotfiles /opt/dotfiles-test

RUN chmod +x /opt/dotfiles-test/entrypoint.py

USER tester
WORKDIR /workspace

ENTRYPOINT ["python3", "/opt/dotfiles-test/entrypoint.py"]
