#!/usr/bin/env bash

set -euo pipefail

AEROSPACE_BIN="${AEROSPACE_BIN:-aerospace}"
LAPTOP_MONITOR_NAME="${AEROSPACE_LAPTOP_MONITOR_NAME:-Built-in Retina Display}"

focused_monitor_name="$($AEROSPACE_BIN list-monitors --focused --format '%{monitor-name}')"
current_workspace="$($AEROSPACE_BIN list-workspaces --focused --format '%{workspace}')"

if [ "$focused_monitor_name" = "$LAPTOP_MONITOR_NAME" ]; then
    target_layout='vertical'
else
    target_layout='horizontal'
fi

for workspace in 1 2 3 4; do
    "$AEROSPACE_BIN" workspace "$workspace" >/dev/null 2>&1 || continue
    "$AEROSPACE_BIN" layout "$target_layout" >/dev/null 2>&1 || true
    "$AEROSPACE_BIN" balance-sizes >/dev/null 2>&1 || true
done

"$AEROSPACE_BIN" workspace "$current_workspace" >/dev/null 2>&1 || true
