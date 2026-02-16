---
title: Commands
description: "Commands invoke. User-initiated entry points that load specific instructions and workflows on demand."
---

# Commands

> Commands invoke. They are user-initiated entry points — markdown files that become slash commands, loading specific instructions and workflows on demand. Where skills activate automatically based on context, commands activate because a human asked.

> **Platform note:** Commands work on both Claude Code and Cowork. Plugins that use commands without hooks or LSP dependencies are compatible with both platforms.

## What It Is

Commands are markdown files that become slash commands. The filename (minus `.md`) becomes the command name. When a user types `/command-name`, the file's content is loaded as instructions for Claude. Commands are the explicit, user-triggered counterpart to skills — they don't activate based on context; they activate because someone typed the name.

Commands support variable substitution: `$ARGUMENTS` captures the full argument string, and positional variables `$1`, `$2`, etc. capture individual arguments.

## When to Use (and When Not To)

| Situation | Use | Reason |
|-----------|-----|--------|
| User-triggered workflow with specific steps | **Command** | Explicit invocation, clear entry point |
| Knowledge that should inform reasoning automatically | Skill | Skills activate on context; commands wait to be called |
| Behavior that must happen every time | Hook | Deterministic enforcement, no user action needed |
| Focused delegation with constrained tools | Agent | Agents scope tools and context; commands scope instructions |
| One-off instruction | Prompt | No mechanism needed |

Key distinction: skills activate when relevant context appears; commands activate when a human types the name. If the workflow should happen without being asked, it's a skill. If it should happen because someone explicitly asked, it's a command.

## How It Works

### Command Anatomy

A command is a markdown file placed in the `commands/` directory:

```
commands/
├── review.md        → /review
├── deploy.md        → /deploy
└── new-feature.md   → /new-feature
```

The filename becomes the slash command name. The markdown content becomes the prompt loaded when the command is invoked.

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `$ARGUMENTS` | Full argument string | `/review src/auth.ts` → `$ARGUMENTS` = `src/auth.ts` |
| `$1` | First positional argument | `/deploy staging` → `$1` = `staging` |
| `$2` | Second positional argument | `/deploy staging v2.1` → `$2` = `v2.1` |

Variables are substituted before the content is sent to Claude. Use them to make commands flexible without making them vague.

### Example Command

A `commands/review.md` file:

```markdown
Review the file at $1 for:

1. Correctness — does the logic do what it claims?
2. Clarity — can a stranger read this without asking questions?
3. Conventions — does it follow the project's patterns?

Report findings as a numbered list. Don't suggest rewrites unless the code is wrong.
```

Invoked with `/review src/auth.ts`, Claude receives the content with `$1` replaced by `src/auth.ts`.

## Configuration

Where commands live:

| Location | Path | Applies To |
|----------|------|------------|
| Personal | `~/.claude/commands/<name>.md` | All your projects |
| Project | `.claude/commands/<name>.md` | This project only |
| Plugin | `<plugin>/commands/<name>.md` | Where plugin is enabled |

Use `/commands` to list available commands.

## Patterns

### Workflow Entry Point

A command that kicks off a multi-step workflow — deployment, release, review cycle. The command carries the procedure; the user triggers it when the time is right.

### Parameterized Task

A command that uses `$ARGUMENTS` or positional variables to scope work to specific files, components, or configurations. Flexible without being vague.

### Opinionated Procedure

A command that encodes a specific, considered way of doing something — how to review code, how to write a commit message, how to debug a failure. The opinion lives in the command; the user opts in by invoking it.

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| **Auto-trigger command** | Commands that should really be skills | If it should happen without being asked, make it a skill |
| **Empty wrapper** | Command that just says "do X" with no guidance | Add the opinionated procedure — that's the value |
| **Kitchen sink** | Command that tries to do everything | One command = one workflow. Split concerns. |
| **Missing variables** | Hardcoded paths or names that should be arguments | Use `$1`, `$2` for anything that varies between invocations |

## Our Opinions

- **Commands are explicit.** They don't guess, they don't auto-trigger, they don't activate on context. A human typed the name. Respect that intent.
- **One command = one workflow.** If you can't name what the command does in two words, the scope is wrong.
- **Commands carry opinions.** A `/review` command doesn't just say "review this" — it says how to review, what to look for, what to report. The opinion is the value.
- **Use skills for automatic, commands for explicit.** If Claude should apply knowledge whenever it's relevant, that's a skill. If Claude should follow a procedure when asked, that's a command.

## References

- [Doctrine](../doctrine.md) § The Six Primitives
- Official Claude Code custom slash commands documentation: `code.claude.com/docs/slash-commands` (fetch locally via `scripts/fetch-claude-code-docs.py`)
