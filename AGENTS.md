# Agent Instructions

This project uses **bd (beads)** for issue tracking.
Run `bd prime` at the start of each session for full workflow context.

---

## Core Principles

* **All work is tracked in bd**
* **Work is performed per issue (task unit)**
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

## Quick Reference

```bash
bd ready                # Find available work
bd show <id>            # View issue details
bd update <id> --claim  # Claim work atomically
bd close <id>           # Complete work
```

---

## Task Workflow (MANDATORY)

For every task (bd issue), follow this exact sequence:

1. **Select work**

   ```bash
   bd ready
   bd show <id>
   ```

2. **Claim**

   ```bash
   bd update <id> --claim
   bd note <id> "agent:<name> claimed this issue"
   ```

3. **Implement**

4. **Validate (if applicable)**

   * Run tests
   * Run linters
   * Ensure build passes

5. **Commit (REQUIRED for every completed task)**

   ```bash
   git add -A
   git commit
   ```

   ### Commit Message Rules (STRICT)

   Commit messages MUST be:

   * Descriptive and structured
   * Written in full sentences
   * Include **what, why, and context**
   * Include references to the bd issue ID
   * Include **agent identification**

   #### Format:

   ```
   <type>: <short summary> (bd:<id>) [agent:<name>]

   <detailed explanation>
   - What was changed
   - Why the change was necessary
   - Any important implementation notes

   Agent: <name>

   <optional: side effects / limitations / follow-ups>
   ```

   #### Example:

   ```
   fix: prevent crash when config is missing (bd:123) [agent:gemini-cli]

   Added null checks when loading configuration files to avoid runtime panic.
   This issue occurred when users launched the app without initializing config.

   Agent: gemini-cli

   Also updated error messages to provide clearer guidance.
   ```

6. **Close issue**

   ```bash
   bd close <id>
   bd note <id> "agent:<name> closed this issue"
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

## Beads Rules

* Use `bd` for ALL task tracking

* Do NOT use:

  * TodoWrite
  * Markdown TODOs
  * External trackers

* Use:

  ```bash
  bd remember
  ```

  for persistent knowledge

* Always record agent activity via `bd note`

---

## Session End Protocol

When ending a session:

1. Ensure ALL completed work is committed
2. Ensure bd issues are properly closed or updated
3. Ensure no working changes remain:

   ```bash
   git status
   ```

   should not show unfinished work

---

## Summary

* Work = bd issue
* One issue → one logical commit
* Commit immediately after completion
* Never push
* Always write high-quality commit messages
* ALWAYS record agent identity in:
  - commit message
  - bd note
