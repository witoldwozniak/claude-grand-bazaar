---
title: Agents
description: "Agents focus. Master craftsmen that each work a single trade with their own tools and skills."
---

# Agents

> Agents focus. They are the master craftsmen — each one works a single trade with their own tools and skills. The craft earns the focus, and the focus earns the output.

## What It Is

Agents are subagents that run in isolated context with constrained tools, specific system prompts, and optional skill loading. They delegate focused work from the main conversation — an architect agent thinks about structure, a security agent scans for vulnerabilities, a reviewer agent reads code. Each stays in its lane.

Agents are defined as markdown files with YAML frontmatter (the spec) and a markdown body (the system prompt).

## When to Use (and When Not To)

| Situation | Use | Reason |
|-----------|-----|--------|
| Repeated delegation of a coherent concern | **Agent** | Focused context, constrained tools, reusable |
| One-off research or exploration | Task tool directly | Creating an agent for single use is overhead |
| Knowledge Claude needs to reason | Skill | Skills inform; agents act |
| Mandatory enforcement | Hook | Agents can forget; hooks can't |
| Simple isolated task | `context: fork` on a skill | Lighter than a full agent definition |

Agents earn their existence through repeated delegation. If you'd only use it once, it's not worth the definition.

## Roles Are Functional, Not Theatrical

Roles are useful when they constrain attention. An architect agent isn't cosplaying — it's a craftsman that deliberately ignores implementation detail to think about structure. The theatrics become harmful when they add ceremony without adding focus, or when agents "discuss" things for the appearance of rigor rather than producing better output.

**The principle: roles must earn their existence by producing meaningfully different output than an unscoped agent would.**

Agent teams — where a lead coordinates specialized teammates working in parallel — are legitimate orchestration, not simulation. The question is always whether the structure produces better work, not whether it looks impressive.

## How It Works

### Subagent Anatomy

An agent is a markdown file with YAML frontmatter and a system prompt body:

```yaml
---
name: code-reviewer
description: Reviews code changes for correctness and style
model: sonnet
tools: Read, Grep, Glob
---

You are a code reviewer. Focus on correctness, clarity, and adherence
to project conventions. Never suggest implementation changes — only
identify problems and explain why they matter.
```

**Key frontmatter fields:**

| Field | Description |
|-------|-------------|
| `name` | Agent identifier. Lowercase, hyphens, max 64 chars. |
| `description` | What the agent does and when to invoke it. Use proactive trigger words. |
| `tools` | Comma-separated tool list. Grant only what's needed. |
| `model` | `sonnet`, `opus`, `haiku`, or inherit from parent. |
| `color` | Terminal color for visual distinction. |
| `skills` | Skills preloaded into the agent's context at startup. |
| `hooks` | Hooks scoped to this agent's lifecycle. |
| `mcpServers` | MCP servers available to this agent. |
| `maxTurns` | Turn limit before the agent must return. |

### Tool Control

Grant minimal access. A reviewer doesn't need Write. A researcher doesn't need Bash.

- **Allowlist**: `tools: Read, Grep, Glob` — only these tools available
- **Denylist**: `tools: ~Bash, ~Write` — everything except these
- **Combined**: `tools: Read, Grep, ~Bash(rm *)` — allow some, deny specific patterns

### Permission Modes

| Mode | Behavior | Use When |
|------|----------|----------|
| `default` | Asks for permission on sensitive operations | Standard work |
| `acceptEdits` | Auto-approves file edits, asks for other actions | Trusted editing tasks |
| `plan` | Read-only, no modifications | Research and planning |
| `dontAsk` | Skips tools it can't auto-approve | Background tasks |
| `bypassPermissions` | No permission checks | **Only with PreToolUse hooks** |

### Model Selection

| Model | When to Use |
|-------|------------|
| **inherit** (default) | Use parent's model. The safe default. |
| **sonnet** | Fast, capable. Good for most focused tasks. |
| **opus** | Maximum capability. Complex reasoning, architectural decisions. |
| **haiku** | Fast and cheap. Simple, well-scoped tasks. |

### Execution Modes

**Foreground** (default) — agent runs, main conversation waits, result returns to context. Suitable for most tasks.

**Background** (`run_in_background: true`) — agent runs independently, main conversation continues. Check results later. Note: MCP tools are unavailable in background subagents. Context compaction can introduce artifacts in long-running background agents.

## Configuration

Where agents live:

| Location | Path |
|----------|------|
| Project | `.claude/agents/<name>.md` |
| Personal | `~/.claude/agents/<name>.md` |
| Plugin | `<plugin>/agents/<name>.md` |

Use `/agents` command to list available agents. Agents from `--add-dir` directories are auto-discovered.

## Coordination

### Escalation Triggers

Flag for Code Actual when:

- New pattern not in existing ADRs
- Significant tech choice (hard to reverse)
- Cross-cutting concerns (auth, logging, observability)
- Scope creep or conflicting requirements
- "I don't know how this should work"

### Large Operations

Operations with **10+ agent spawns** require a persistent plan file:

**File:** `plans/{operation-name}.md`

**Required sections:**

- Mission parameters (total agents, batches, rounds)
- Current progress tracker (checkboxes or status table)
- Batch assignments with completion status
- Quarantine/exception list

**Why:** Without a readable plan file, Code Actual cannot track progress or understand remaining work. Rounds get skipped unintentionally, state becomes unclear, and coordination fails.

**Update cadence:** After each batch completes or when status changes.

## Patterns

### Lead + Specialist Teams

A lead agent coordinates specialized teammates working in parallel. Each specialist has its own tools and skills. The lead delegates, collects results, and synthesizes. Legitimate orchestration, not simulation.

### Read-Only Reviewers

Review agents get only Read, Grep, Glob — never Write or Edit. A reviewer that can modify code blurs the boundary between review and implementation.

### Skill-Loaded Specialists

Agents can preload skills via the `skills` frontmatter field. The full skill content is injected at startup, giving the agent domain expertise without reproducing it in the system prompt. Example: a testing agent preloads the TDD skill.

### Scoped Hooks on Agents

Agents can define hooks in their frontmatter that only apply during the agent's lifecycle. `Stop` hooks on agents automatically become `SubagentStop` hooks. Use this for quality gates: the agent can't finish until its hook-checked conditions pass.

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| **Swiss-army agent** | Too many tools, too broad a scope | One agent = one trade. Split concerns. |
| **Write tools on reviewer** | Reviewer modifies code, blurs responsibility | Read-only tool access for reviewers |
| **bypassPermissions without hooks** | No safety net on unrestricted access | Always pair with PreToolUse hooks |
| **Single-use agent** | Overhead of definition for one invocation | Use Task tool directly |
| **Vague description** | Claude doesn't know when to delegate to it | Use proactive trigger words and explicit use cases |
| **Giant system prompt** | Context bloat, diluted focus | Use skills for knowledge; keep system prompt focused on role and constraints |
| **Expecting conversation context** | Subagents don't see the main conversation | Provide all necessary context in the delegation prompt |

## Our Opinions

- **One agent = one trade.** If you can't name the craft in two words, the scope is wrong.
- **Start with skills.** Only create an agent when the focus genuinely improves output. Many tasks work fine with a skill loaded into the main conversation.
- **Read-only for review.** Never give a reviewer write access. Review and implementation are separate concerns.
- **Every agent using `bypassPermissions` must have PreToolUse hooks.** No exceptions. Unrestricted access without guardrails is how incidents happen.
- **Agents load skills at startup — use this.** Don't repeat skill content in the system prompt. Preload the skill and let it do its job.
- **Roles are earned, not assigned.** If an agent doesn't produce meaningfully different output than an unscoped agent, it doesn't need to exist.

## References

- `plugins/plugin-authoring/skills/create-agents/` — comprehensive agent creation guide
- `plugins/plugin-authoring/agents/` — living examples (agent-creator, hook-author, skill-manager, etc.)
- [Doctrine](../doctrine.md) § The Six Primitives, § On Roles and Theater
- Official Claude Code sub-agents documentation: `code.claude.com/docs/sub-agents` (fetch locally via `scripts/fetch-claude-code-docs.py`)
