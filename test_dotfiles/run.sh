#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd -P)"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/setup-smoke-$(date +%Y%m%d-%H%M%S).log"
IMAGE_NAME="dotfiles-linux-test"

mkdir -p "$LOG_DIR"
exec > >(tee "$LOG_FILE") 2>&1

if [ "$#" -gt 0 ]; then
    printf 'usage: %s\n' "$0" >&2
    exit 1
fi

printf 'Writing smoke test log to %s\n' "$LOG_FILE"
printf 'Building Docker image %s from %s\n' "$IMAGE_NAME" "$SCRIPT_DIR"
docker build -t "$IMAGE_NAME" -f "$SCRIPT_DIR/Dockerfile" "$SCRIPT_DIR"

printf 'Running setup smoke test in Docker\n'
docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp/dotfiles-test-home -v "$REPO_ROOT:/workspace:ro" "$IMAGE_NAME"
