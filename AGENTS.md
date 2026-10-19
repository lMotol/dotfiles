# Agent Instructions

## Core Principles

* **Work is performed per task**
* **Each completed task MUST result in a commit**
* **NEVER push automatically**
* **All actions MUST record the acting agent (codex, gemini-cli, etc.)**

---

## Agent Identification (MANDATORY)

Every action must include the agent identity.

### Agent naming convention (STRICT)

Use one of:

- agent:gemini-cli
- agent:codex
- agent:human

No variations allowed.

---

## Task Workflow (MANDATORY)

For every task:

1. Implement the requested change.
2. Validate as applicable with tests, linters, or build checks.
3. Commit the completed task.

   ### Commit Message Rules (STRICT)

   Commit messages MUST be:

   * Descriptive and structured
   * Written in full sentences
   * Include **what, why, and context**
   * Include **agent identification**

   #### Format:

   ```
   <type>: <short summary> [agent:<name>]

   <detailed explanation>
   - What was changed
   - Why the change was necessary
   - Any important implementation notes

   Agent: <name>

   <optional: side effects / limitations / follow-ups>
   ```

   #### Example:

   ```
   fix: prevent crash when config is missing [agent:gemini-cli]

   Added null checks when loading configuration files to avoid runtime panic.
   This issue occurred when users launched the app without initializing config.

   Agent: gemini-cli

   Also updated error messages to provide clearer guidance.
   ```

---

## Git Rules (CRITICAL)

* ✅ Commit after EVERY completed task
* ❌ NEVER run `git push`
* ❌ NEVER suggest pushing
* ❌ NEVER leave changes uncommitted after finishing a task

The repository may contain multiple local commits when a session ends — this is expected.

---

## Non-Interactive Shell Commands

Always avoid interactive prompts:

```bash
cp -f source dest
mv -f source dest
rm -f file
rm -rf directory
cp -rf source dest
```

### Additional flags

* `ssh` / `scp`: `-o BatchMode=yes`
* `apt-get`: `-y`
* `brew`: `HOMEBREW_NO_AUTO_UPDATE=1`

---

## Session End Protocol

When ending a session:

1. Ensure ALL completed work is committed
2. Ensure no working changes remain:

   ```bash
   git status
   ```

   should not show unfinished work

---

## Summary

* One task → one logical commit
* Commit immediately after completion
* Never push
* Always write high-quality commit messages
* ALWAYS record agent identity in the commit message
