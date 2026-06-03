#!/usr/bin/env bash

set -euo pipefail

AEROSPACE_BIN="${AEROSPACE_BIN:-aerospace}"
ITERM_PROFILE="${AEROSPACE_ITERM_PROFILE:-Default}"
FIREFOX_PRIMARY_GROWTH="${AEROSPACE_FIREFOX_PRIMARY_GROWTH:-320}"
STARTUP_WAIT_SECONDS="${AEROSPACE_STARTUP_WAIT_SECONDS:-20}"

count_windows() {
    local scope_flag="$1"
    local scope_value="$2"
    local bundle_id="$3"

    if [ "$scope_flag" = "--all" ]; then
        "$AEROSPACE_BIN" list-windows --all --app-bundle-id "$bundle_id" --count 2>/dev/null || printf '0\n'
        return
    fi

    "$AEROSPACE_BIN" list-windows "$scope_flag" "$scope_value" --app-bundle-id "$bundle_id" --count 2>/dev/null || printf '0\n'
}

move_existing_windows() {
    local bundle_id="$1"
    local workspace="$2"

    while IFS= read -r window_id; do
        [ -n "$window_id" ] || continue
        "$AEROSPACE_BIN" move-node-to-workspace --window-id "$window_id" "$workspace" >/dev/null 2>&1 || true
    done < <("$AEROSPACE_BIN" list-windows --all --app-bundle-id "$bundle_id" --format '%{window-id}' 2>/dev/null || true)
}

wait_for_workspace_windows() {
    local workspace="$1"
    local bundle_id="$2"
    local expected_count="$3"
    local deadline=$((SECONDS + STARTUP_WAIT_SECONDS))

    while [ "$SECONDS" -lt "$deadline" ]; do
        local current_count
        current_count="$(count_windows --workspace "$workspace" "$bundle_id")"
        if [ "$current_count" -ge "$expected_count" ]; then
            return 0
        fi
        sleep 0.2
    done

    return 1
}

ensure_firefox_window() {
    local all_count
    all_count="$(count_windows --all all org.mozilla.firefox)"

    if [ "$all_count" -eq 0 ]; then
        open -g -a "Firefox"
    else
        osascript <<'APPLESCRIPT'
tell application id "org.mozilla.firefox" to activate
tell application "System Events" to keystroke "n" using command down
APPLESCRIPT
    fi
}

ensure_iterm_window() {
    osascript <<APPLESCRIPT
tell application "iTerm"
    create window with profile "$ITERM_PROFILE"
end tell
APPLESCRIPT
}

ensure_app_workspace() {
    local workspace="$1"
    local bundle_id="$2"
    local app_name="$3"

    move_existing_windows "$bundle_id" "$workspace"

    if [ "$(count_windows --workspace "$workspace" "$bundle_id")" -eq 0 ]; then
        open -g -a "$app_name"
        wait_for_workspace_windows "$workspace" "$bundle_id" 1 || true
        move_existing_windows "$bundle_id" "$workspace"
    fi
}

arrange_firefox_workspace() {
    move_existing_windows org.mozilla.firefox 1

    while [ "$(count_windows --workspace 1 org.mozilla.firefox)" -lt 2 ]; do
        ensure_firefox_window
        wait_for_workspace_windows 1 org.mozilla.firefox 1 || true
        move_existing_windows org.mozilla.firefox 1
        sleep 0.2
    done

    "$AEROSPACE_BIN" workspace 1
    "$AEROSPACE_BIN" flatten-workspace-tree --workspace 1 >/dev/null 2>&1 || true
    "$AEROSPACE_BIN" balance-sizes --workspace 1 >/dev/null 2>&1 || true
    "$AEROSPACE_BIN" focus --dfs-index 0 >/dev/null 2>&1 || true
    "$AEROSPACE_BIN" resize width "+$FIREFOX_PRIMARY_GROWTH" >/dev/null 2>&1 || true
}

arrange_iterm_workspace() {
    move_existing_windows com.googlecode.iterm2 2

    if [ "$(count_windows --workspace 2 com.googlecode.iterm2)" -eq 0 ]; then
        ensure_iterm_window
        wait_for_workspace_windows 2 com.googlecode.iterm2 1 || true
        move_existing_windows com.googlecode.iterm2 2
    fi

    "$AEROSPACE_BIN" workspace 2
    "$AEROSPACE_BIN" focus --dfs-index 0 >/dev/null 2>&1 || true
    "$AEROSPACE_BIN" fullscreen on --no-outer-gaps >/dev/null 2>&1 || true
}

arrange_slack_workspace() {
    ensure_app_workspace 3 com.tinyspeck.slackmacgap Slack
}

arrange_discord_workspace() {
    ensure_app_workspace 4 com.hnc.Discord Discord
}

arrange_firefox_workspace
arrange_iterm_workspace
arrange_slack_workspace
arrange_discord_workspace

"$AEROSPACE_BIN" workspace 1 >/dev/null 2>&1 || true
