#!/bin/bash
# OpenAI Codex CLI インストールスクリプト

TOOL_NAME="Codex CLI"
COMMAND_NAME="codex"

if ! command -v npm &>/dev/null; then
    echo "Error: npm is not installed"
    echo "Please install Node.js and npm first:"
    echo "  macOS: brew install node"
    echo "  Linux: sudo apt install nodejs npm (Ubuntu/Debian)"
    exit 1
fi

echo "Installing $TOOL_NAME via npm..."

npm install -g @openai/codex@latest

echo ""
if command -v "$COMMAND_NAME" &>/dev/null; then
    echo "✓ $TOOL_NAME installation successful!"
    echo "Next steps:"
    echo "  1. Run: codex auth"
    echo "  2. Start using: codex"
else
    echo "⚠ Installation completed. Please reload your shell."
fi
