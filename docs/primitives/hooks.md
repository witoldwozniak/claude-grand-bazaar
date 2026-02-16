---
title: Hooks
description: "Hooks enforce. Automated guardrails that run whether the agent remembers to or not."
---

# Hooks

> Hooks enforce. They are automated guardrails that run whether the agent remembers to or not. If a behavior must happen every time, it belongs in a hook.

> **Platform note:** Hooks are a Claude Code feature. Cowork does not support hooks. Plugins that rely on hooks for enforcement are Claude Code-only.

## What It Is

Hooks are user-defined shell commands or LLM prompts that execute automatically at specific points in Claude Code's lifecycle. They provide **deterministic control** — unlike prompt-based instructions that an LLM might ignore due to context pressure or conflicting signals, hooks guarantee execution. Prompts are suggestions; hooks are guarantees.

Real-world consequences of relying on prompts alone: $30,000 in fraudulent API charges from hardcoded keys, home directories nuked by `rm -rf ~/`, tests modified to pass with incorrect behavior. Hooks prevent these.

## When to Use (and When Not To)

| Situation | Use | Reason |
|-----------|-----|--------|
| Must happen every time | **Hook** | Deterministic — no chance of being skipped |
| Should inform Claude's thinking | Skill | Advisory — shapes reasoning, not enforcement |
| One-off instruction | CLAUDE.md / prompt | No mechanism needed |
| Context-dependent recommendation | Skill or prompt | Hooks are for rules, not suggestions |
| Blocking a dangerous action | **Hook** (PreToolUse) | Only enforcement mechanism that can prevent tool execution |

Key insight: "Claude will read 'NEVER edit .env files' in CLAUDE.md, understand it, and might still edit your .env file because of context pressure." Only hooks provide deterministic protection.

## How It Works

### Hook Events

Hooks fire at specific points during a Claude Code session. The events, their timing, and their capabilities:

| Event | When It Fires | Matchers | Can Block |
|-------|---------------|----------|-----------|
| **SessionStart** | Session begins or resumes | startup/resume/clear/compact | No |
| **UserPromptSubmit** | User submits prompt, before processing | No | Yes |
| **PreToolUse** | Before tool execution | Tool names | Yes |
| **PermissionRequest** | Permission dialog appears | Tool names | Yes |
| **PostToolUse** | After tool succeeds | Tool names | No (already ran) |
| **PostToolUseFailure** | After tool fails | Tool names | No |
| **Notification** | Claude sends alert | Notification type | No |
| **SubagentStart** | Subagent spawned | Agent type | No |
| **SubagentStop** | Subagent finishes | Agent type | Yes |
| **Stop** | Main agent finishes responding | No | Yes (forces continue) |
| **TeammateIdle** | Team teammate about to go idle | No | Yes |
| **TaskCompleted** | Task marked as completed | No | Yes |
| **PreCompact** | Before context compaction | manual/auto | No |
| **SessionEnd** | Session terminates | Exit reason | No |

**PreToolUse** is the primary control point — it receives the tool name and all parameters, letting you block, modify, or approve operations before they execute.

**Stop hooks** deserve attention: exit code 2 forces Claude to continue working. Check the `stop_hook_active` flag to prevent infinite loops.

### Hook Types

| Type | Use When | How It Works |
|------|----------|--------------|
| **command** | Rule is deterministic / programmable | Shell command, JSON via stdin, exit codes decide |
| **prompt** | Decision needs LLM judgment | Single-turn LLM query (Haiku by default), returns approve/block |
| **agent** | Verification needs file inspection | Multi-turn subagent with tools (Read, Grep, Glob), up to 50 turns |

Default to **command** hooks. Use prompt/agent only when the decision genuinely requires understanding intent or inspecting codebase state.

### Matchers

Matchers are **regular expressions** and **case-sensitive**. They filter which tool invocations or events trigger a hook.

Common patterns:
- `Write` — exact match for Write tool
- `Edit|Write|MultiEdit` — any file modification tool
- `Notebook.*` — all notebook-related tools
- `mcp__github__.*` — all GitHub MCP server tools
- `mcp__<server>__<tool>` — targeting specific MCP tools

Events without matcher support (UserPromptSubmit, Stop, TeammateIdle, TaskCompleted) fire on every occurrence.

### Exit Codes and Control Flow

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| **0** | Success / allow | Execution continues; stdout parsed for JSON |
| **2** | Block | Action prevented; stderr fed to Claude as context |
| **Other** | Non-blocking error | Logged in verbose mode; execution continues |

Exit code 2 is the enforcement mechanism, but its effect varies by event:

| Event | Can Block | Effect of Exit 2 |
|-------|-----------|-------------------|
| PreToolUse | Yes | Blocks the tool call |
| PermissionRequest | Yes | Denies permission |
| UserPromptSubmit | Yes | Blocks and erases prompt |
| Stop / SubagentStop | Yes | Forces continuation |
| TeammateIdle | Yes | Prevents idle, teammate continues |
| TaskCompleted | Yes | Prevents task completion |
| PostToolUse | No | Shows stderr to Claude (tool already ran) |
| SessionStart/End | No | Shows stderr to user only |

### JSON Output

Beyond exit codes, hooks can return structured JSON to stdout for finer-grained control:

**PreToolUse** uses `hookSpecificOutput`:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Safe operation",
    "updatedInput": { "command": "npm run lint --fix" }
  }
}
```

The `updatedInput` field lets you intercept and transform commands before execution — automatically adding safety flags, redirecting operations, etc.

**Stop / PostToolUse** use top-level `decision`:
```json
{
  "decision": "block",
  "reason": "Tests must pass before completing"
}
```

**Universal fields** (all events): `continue` (false stops Claude entirely), `stopReason`, `systemMessage`, `suppressOutput`.

### Environment Variables

| Variable | Description | Availability |
|----------|-------------|--------------|
| `$CLAUDE_PROJECT_DIR` | Absolute path to project root | All hooks |
| `$CLAUDE_PLUGIN_ROOT` | Plugin directory path | Plugin hooks only |
| `$CLAUDE_CODE_REMOTE` | `"true"` in web environments | All hooks |
| `$CLAUDE_ENV_FILE` | Path to persist env vars for session | SessionStart only |

Always use `$CLAUDE_PROJECT_DIR` for script paths — ensures hooks work regardless of cwd.

## Configuration

Hooks can be configured at multiple levels with clear precedence:

1. **Managed settings** (enterprise policies) — highest priority
2. **User settings** (`~/.claude/settings.json`) — global defaults
3. **Project settings** (`.claude/settings.json`) — repository-specific
4. **Local settings** (`.claude/settings.local.json`) — personal, git-ignored
5. **Plugin hooks** (`hooks/hooks.json` in plugin root)
6. **Skill/agent frontmatter** — scoped to component lifecycle

Configuration schema nests hook definitions under event names, with matchers filtering triggers:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

For plugin hooks, use `${CLAUDE_PLUGIN_ROOT}` for portable script paths.

Hooks are **captured at session startup** — modifications to settings files don't take effect until restart. This is a security feature preventing malicious mid-session modifications.

## Language Choice

| Language | Startup Time | Best For |
|----------|-------------|----------|
| **Bash** | 10-20ms | Simple checks, flag files, git operations |
| **Node.js** | 50-100ms | High-frequency events (PreToolUse), complex JSON |
| **Python** | 200-400ms | JSON parsing, infrequent events, readability |

Python is preferred for most hooks — startup cost matters less than correctness and maintainability. Use Bash only for truly simple checks. Node when PreToolUse frequency makes Python's startup cost noticeable.

## Patterns

### Security Blocking (PreToolUse → Bash)

Block dangerous commands before they execute:

```python
dangerous = [
    r'rm\s+.*-[rf].*\s+[~/]',
    r'curl.*\|\s*sh',
    r'chmod\s+777',
]
for pattern in dangerous:
    if re.search(pattern, command, re.IGNORECASE):
        print(f"BLOCKED: {pattern}", file=sys.stderr)
        sys.exit(2)
```

### Context Injection (SessionStart)

Load project state when Claude starts — stdout from SessionStart hooks is added to Claude's context:

```json
{
  "SessionStart": [{
    "hooks": [{
      "type": "command",
      "command": "git status --short && echo '---' && cat TODO.md 2>/dev/null"
    }]
  }]
}
```

### Test Enforcement (Stop)

Prevent completion until tests pass:

```json
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "npm test || (echo 'Tests must pass' >&2 && exit 2)"
    }]
  }]
}
```

### Auto-Formatting (PostToolUse → Write|Edit)

Run formatters after file changes. Tradeoff: formatting on every edit adds system messages consuming tokens. Some teams prefer formatting on commit instead.

### Notifications (Notification, async)

Desktop alerts when Claude needs input. Use `"async": true` to prevent blocking:

```json
{
  "Notification": [{
    "hooks": [{
      "type": "command",
      "command": "notify-send 'Claude Code' \"$(jq -r '.message')\"",
      "async": true
    }]
  }]
}
```

### MCP Tool Monitoring (PreToolUse)

Target hooks to specific MCP servers using the `mcp__<server>__<tool>` naming pattern.

### Flag-File Activation

Enable/disable hooks dynamically via flag files — check for a flag at `$CLAUDE_PROJECT_DIR/.enable-<feature>` and exit 0 early when absent.

## Anti-Patterns

| Pitfall | Why It Bites | Fix |
|---------|-------------|-----|
| Case mismatch in matchers | `write` won't match `Write` | Verify exact tool names with `/hooks` |
| Auto-formatting on every edit | System messages consume tokens rapidly | Format on commit instead |
| Exit 2 on PostToolUse | Can't undo a completed operation | Use PreToolUse for blocking |
| No timeout on external hooks | Default is 600s for commands | Set explicit timeouts |
| No `stop_hook_active` check | Stop hooks loop infinitely | Always check the flag |
| Broken hook blocks all work | Non-zero exit halts the session | Default path must exit 0 |
| Trusting prompt instructions for safety | Context pressure can override prompts | Use hooks for anything mandatory |

## Debugging

1. **`claude --debug`** — reveals matcher evaluation, hook timing, exit codes, stdout/stderr
2. **`/hooks` command** — lists all registered hooks and their configuration
3. **`Ctrl+O` verbose mode** — toggle during session to see hook progress in transcript
4. **Manual testing** — pipe JSON to the hook script before deploying:

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"test.txt"}}' | \
  CLAUDE_PROJECT_DIR="$(pwd)" python3 .claude/hooks/my-hook.py
echo $?  # expect 0 for allow, 2 for block
```

## Our Opinions

- **Default to command hooks.** Prompt and agent hooks are for when you genuinely cannot express the rule programmatically. Most enforcement is deterministic.
- **Block at boundaries, not mid-plan.** Hooks work best when they complement rather than fight the AI. Letting Claude complete work and validating at commit boundaries is more effective than interrupting mid-task.
- **Every enforced standard needs a hook.** If a behavior must happen every time, a skill instruction is not enough. Skills suggest; hooks guarantee.
- **Python for hook scripts** unless startup time is critical. Readability and JSON handling matter more than 200ms.
- **Always fail open.** The default code path must be `exit 0`. A broken hook must not block all work.
- **Multiple matching hooks run in parallel.** Design them to be independent — you cannot rely on execution order.

## References

- Karan Bansal, "Claude Code Hooks Guide" (2026-01-27) — community patterns and safety hooks
- "Claude Code hooks: Complete guide to event-driven automation" — comprehensive event reference and real-world patterns
- `plugins/plugin-authoring/agents/hook-author.md` — hook creation agent with templates and constraints
- Official Claude Code hooks documentation: `code.claude.com/docs/hooks` (fetch locally via `scripts/fetch-claude-code-docs.py`)
