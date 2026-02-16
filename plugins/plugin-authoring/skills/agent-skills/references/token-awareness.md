# Token Awareness for Skill Design

Guidance on sizing skill content and managing context costs during development.

## CLAUDE.md Sizing

CLAUDE.md files auto-load at session start — they set the baseline token cost before any work begins.

| Configuration | Token Cost | Notes |
|---------------|-----------|-------|
| Lean (recommended) | 800-1,300 tokens | One-line summary, essential commands, key directories, file boundaries |
| Standard | 2,000-3,500 tokens | Adds workflow preferences, code style, testing procedures |
| Maximum | 5,000 tokens | Hard ceiling — beyond this, diminishing returns |
| Bloated (avoid) | 8,000-11,000 tokens | Common in monolithic configs; wastes 7k+ tokens before coding starts |

One documented case reduced startup context from 11,000 to 1,300 tokens — an 88% reduction freeing 7,200 tokens for actual work.

## MCP Server Context Costs

Each enabled MCP server adds tool definitions to the context window at session start:

- Typical 5-server setup: ~55,000 tokens before any conversation
- Individual servers like Jira alone: ~17,000 tokens
- Use `/context` command to identify which servers contribute most

Disable unused MCP servers using `@server-name disable` or `/mcp` command.

## Compaction Discipline

| Action | When | Effect |
|--------|------|--------|
| `/compact` (manual) | At ~70% context capacity | 50-70% reduction with good summary quality |
| Auto-compact | At ~95% capacity (system-triggered) | Lower quality — less room for good summarization |
| `/clear` | Between unrelated tasks | Complete context reset |

Manual `/compact` at 70% produces significantly better results than waiting for auto-compact at 95%.

## Document & Clear Workflow

For long skill development sessions:

1. Have Claude document progress to a markdown file (completed steps, current state, remaining work)
2. Run `/clear` for complete context reset
3. Start fresh with instruction to read the progress file and continue

This maintains continuity without dragging accumulated history forward.

## Measured Impact

Applying the tiered documentation strategy described in SKILL.md reduces baseline context by approximately 62% compared to monolithic documentation.
