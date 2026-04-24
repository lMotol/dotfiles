#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd -P)"
TMP_HOME="$(mktemp -d /tmp/dotfiles-test-home.XXXXXX)"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/setup-smoke-$(date +%Y%m%d-%H%M%S).log"
KEEP_HOME=0

mkdir -p "$LOG_DIR"
exec > >(tee "$LOG_FILE") 2>&1

cleanup() {
    if [ "$KEEP_HOME" -eq 0 ]; then
        rm -rf "$TMP_HOME"
    else
        printf 'Preserved test HOME at %s\n' "$TMP_HOME"
    fi
}

trap cleanup EXIT

if [ "${1:-}" = "--keep-home" ]; then
    KEEP_HOME=1
    shift
fi

if [ "$#" -gt 0 ]; then
    printf 'usage: %s [--keep-home]\n' "$0" >&2
    exit 1
fi

printf 'Writing smoke test log to %s\n' "$LOG_FILE"
printf 'Running setup smoke test with HOME=%s\n' "$TMP_HOME"
HOME="$TMP_HOME" WORKSPACE_DIR="$REPO_ROOT" bash "$SCRIPT_DIR/entrypoint.sh"
