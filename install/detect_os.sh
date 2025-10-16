#!/bin/bash
# OS検出ユーティリティ

detect_os() {
    case "$(uname -s)" in
        Darwin*)
            echo "macos"
            ;;
        Linux*)
            echo "linux"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

detect_arch() {
    uname -m
}

# スクリプトから直接呼ばれた場合
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    detect_os
fi
