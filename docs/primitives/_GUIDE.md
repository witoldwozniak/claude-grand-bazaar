---
title: Primitives Guide
description: "How to pick the right primitive for a given concern. Central reference for cross-primitive decisions."
---

# Primitives Guide

The five primitives — Skills, Hooks, Subagents, Connectors (MCP Servers), and LSP Servers — each solve different problems. This guide helps you pick the right one.

## Concerns Matrix

| Concern | Best Primitive | Why | Not This |
|---------|---------------|-----|----------|
| Domain knowledge Claude needs to reason with | **Skill** | Skills load expertise into context and shape reasoning | Subagent (unless you also need tool isolation) |
| A behavior that must happen every time | **Hook** | Deterministic enforcement — hooks can't be skipped by context pressure | Skill (advisory only, can be ignored) |
| Focused work with constrained tools | **Subagent** | Isolated context window, scoped tool access, dedicated system prompt | Skill (no tool constraints) |
| Persistent connection to an external service | **Connector** | Exposes external APIs as native tools via MCP | Bash script (for one-off calls) |
| Real-time code diagnostics and intelligence | **LSP Server** | Continuous analysis, inline feedback, IDE integration | Hook (event-driven, not continuous) |
| Blocking a dangerous tool invocation | **Hook** (PreToolUse) | Only mechanism that can prevent tool execution before it happens | Skill or CLAUDE.md (advisory, not enforced) |
| Verbose output that would pollute context | **Subagent** | Results stay in subagent's context; only summary returns to caller | Main conversation (context bloat) |
| Project conventions and style guidance | **Skill** | Informs reasoning without enforcing; flexible application | Hook (too rigid for stylistic guidance) |
| Mandatory linting or formatting after edits | **Hook** (PostToolUse) | Runs automatically after file changes, no agent cooperation needed | Skill (agent might skip it under pressure) |
| Database queries or API exploration | **Connector** | Structured tool interface, consistent access patterns | Subagent with Bash (less structured) |
| One-off research or exploration | **Task tool** directly | No definition overhead for single-use work | Subagent (unnecessary setup cost) |
| Simple isolated task with skill context | **Skill** with `context: fork` | Lighter than a full subagent definition | Subagent (overhead not justified) |

## Quick Decision Flow

1. **Must it happen every time, regardless of context?** → Hook
2. **Does it need external system access?** → Connector (MCP Server)
3. **Does it need real-time code analysis?** → LSP Server
4. **Does it need isolated context and constrained tools?** → Subagent
5. **Does it need to inform Claude's reasoning?** → Skill

## Primitive References

- [Skills](SKILLS.md) — knowledge and reasoning loaded into context
- [Hooks](HOOKS.md) — automated guardrails and enforcement
- [Subagents](SUBAGENTS.md) — focused specialists with isolated context
- [Connectors (MCP Servers)](MCP.md) — external tool and API connections
- [LSP Servers](LSP.md) — real-time code intelligence
