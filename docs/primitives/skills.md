---
title: Skills
description: "Skills inform. They carry knowledge and reasoning into Claude's context to shape how it thinks about problems."
---

# Skills

> Skills inform. They carry knowledge and reasoning — how to think about a problem, what to know, what steps to follow.

## What It Is

Skills are markdown documents that load into Claude's context to inform reasoning. They are the knowledge layer — they shape how Claude thinks about problems, what conventions it follows, and what steps it takes. A skill carries expertise; Claude applies it.

Skills follow the [Agent Skills](https://agentskills.io) open standard. Claude Code extends the standard with invocation control, subagent execution, and dynamic context injection.

## When to Use (and When Not To)

| Situation | Use | Reason |
|-----------|-----|--------|
| Claude needs domain knowledge | **Skill** | Loads expertise into context |
| A behavior must happen every time | Hook | Skills are advisory; hooks are deterministic |
| Work needs isolated focus | Agent | Agents constrain tools and context |
| Persistent project context | CLAUDE.md | Always loaded, no invocation needed |
| One-off instruction | Prompt | No mechanism needed |

Key distinction: skills suggest, hooks guarantee. If something MUST happen, it's a hook. If something should INFORM how Claude thinks, it's a skill.

## Skill Categories

From doctrine, skills fall into these categories:

- **Docs-as-skill** — domain knowledge, conventions, style guides. The skill carries what Claude doesn't already know about a domain.
- **Workflows** — step-by-step procedures for specific tasks. Debugging workflows, deployment procedures, review checklists.
- **Conventions** — coding standards, naming patterns, architectural decisions. How this project does things.
- **Reasoning frameworks** — structured thinking approaches. Toulmin argumentation, pre-mortem analysis, competing hypotheses.

These are tags that communicate intent and guide form, not rigid templates.

## How It Works

### Progressive Disclosure

Skills use a three-level loading system — the core mechanism for managing context cost:

1. **Metadata (name + description)** — always in context (~100 words). Claude uses this to decide when to load the skill.
2. **SKILL.md body** — loaded when the skill triggers (<5,000 words). The main instructions.
3. **Bundled resources** — loaded as needed. Scripts execute without loading into context; references load only when Claude needs them.

The test: "Could this section move to a reference without hurting Claude's ability to route?" If yes, move it.

### SKILL.md Structure

Every skill needs a `SKILL.md` file with two parts: YAML frontmatter and markdown content.

**Key frontmatter fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name (defaults to directory name). Lowercase, hyphens, max 64 chars. |
| `description` | Recommended | What the skill does and when to use it. Claude uses this for auto-loading. |
| `disable-model-invocation` | No | `true` = only user can invoke (e.g., `/deploy`). Default: `false`. |
| `user-invocable` | No | `false` = only Claude can invoke (background knowledge). Default: `true`. |
| `allowed-tools` | No | Tools Claude can use without permission when skill is active. |
| `context` | No | `fork` = run in isolated subagent context. |
| `agent` | No | Which subagent type when `context: fork`. Default: `general-purpose`. |
| `hooks` | No | Hooks scoped to this skill's lifecycle. |

### Description as Trigger

The description is the primary triggering mechanism. It must answer WHAT the skill does and WHEN to use it. Include keywords matching natural user phrasings:

```yaml
description: |
  Guide for creating, evaluating, and improving agent skills. Use when
  creating a new skill, updating an existing skill, writing SKILL.md files,
  or reviewing skill design. Triggers: "create a skill", "evaluate this
  skill", "improve this skill".
```

### Bundled Resources

Skills can include supporting files in their directory:

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── references/        # Loaded on demand (detailed docs, examples)
├── scripts/           # Executed, not loaded into context
└── assets/            # Templates, output formats
```

Reference supporting files from SKILL.md so Claude knows what each contains and when to load it. Keep SKILL.md under ~500 lines — move depth to references.

### Variable Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill |
| `$ARGUMENTS[N]` | Specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `${CLAUDE_SESSION_ID}` | Current session ID |

**Dynamic context injection** with `!command!` syntax runs shell commands before the skill content is sent to Claude — the output replaces the placeholder:

```markdown
## Current state
- Branch: !`git branch --show-current`
- Status: !`git status --short`
```

### Structure Patterns

**Narrow skill** — single concern, focused instructions. SKILL.md under ~500 lines. One job done well.

**Meta-skill / gateway** — routes to sub-resources based on the task. SKILL.md acts as a decision tree pointing to references/. Can be longer when the additional length is routing infrastructure. Example: `agent-skills` skill routes between creation, evaluation, and improvement workflows.

## Configuration

Where skills live determines their scope:

| Location | Path | Applies To |
|----------|------|------------|
| Enterprise | Managed settings | All users in organization |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin is enabled |

Higher-priority locations win when names conflict: enterprise > personal > project. Plugin skills use `plugin-name:skill-name` namespace, so they cannot conflict with other levels.

Skills in nested `.claude/skills/` directories (e.g., `packages/frontend/.claude/skills/`) are auto-discovered when working in those subdirectories — supports monorepo setups.

## Writing Guidelines

### Concise is Key

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece: "Does this paragraph justify its token cost?" Prefer concise examples over verbose explanations.

### Degrees of Freedom

Match specificity to the task's fragility and variability:

| Freedom Level | When to Use | Form |
|---------------|-------------|------|
| **High** | Multiple approaches valid | Text-based instructions |
| **Medium** | Preferred pattern exists | Pseudocode or parameterized scripts |
| **Low** | Fragile operations, consistency critical | Specific scripts, few parameters |

### Token Budget Awareness

CLAUDE.md files load at session start — target 800-1,300 tokens lean, 5,000 max. SKILL.md follows the same principle. Use tiered documentation — move depth to references, reducing baseline context.

Skill descriptions are loaded into context so Claude knows what's available. Many skills can exceed the character budget (2% of context window, ~16,000 chars fallback). Run `/context` to check for excluded skills.

## Patterns

### Domain Knowledge Skill

Carries expertise Claude doesn't have. Example: `write-for-llms` teaches vocabulary control, structural templates, and disambiguation for LLM-optimized prose.

### Workflow / Procedure Skill

Step-by-step procedure for a specific task. Add `disable-model-invocation: true` for workflows with side effects (deploy, release). Example: a deployment skill that runs tests, builds, and pushes.

### Reasoning Framework Skill

Structured thinking approach. Example: pre-mortem analysis (assume the task failed, explain why), competing hypotheses (evaluate evidence against alternatives).

### Gateway / Router Skill

Routes to sub-resources based on the task at hand. SKILL.md contains the decision tree; references/ contain the depth. Example: `agent-skills` routes between creation, evaluation, and improvement workflows based on what the user asks.

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| **Tutorial** | Teaches Claude what it already knows | Only add what's new |
| **Dump** | Loads everything into SKILL.md | Use progressive disclosure; move depth to references |
| **Orphan** | References not mentioned in SKILL.md | Claude won't know they exist; always reference from SKILL.md |
| **Weak trigger** | Vague description, Claude doesn't know when to load it | Include explicit trigger phrases and keywords |
| **Inline bloat** | Long examples inline instead of in references | Move examples to references/; keep SKILL.md under 500 lines |
| **Wrong location** | Mandatory behavior in a skill | Skills suggest; hooks guarantee. Move enforcement to hooks. |

## Our Opinions

- **Every paragraph must justify its token cost.** Context is finite. If something doesn't make Claude meaningfully better at the task, cut it.
- **Opinionated, not encyclopedic.** Skills take a position on how a domain should work. No hedging, no "you could also try…" equivocation.
- **Progressive disclosure is not optional.** It's how skills scale. Metadata → SKILL.md → references is the loading architecture.
- **If it must happen every time, it's a hook.** Skills inform reasoning; they cannot enforce behavior. A skill that says "always run tests" is a suggestion. A Stop hook that checks test results is a guarantee.
- **Start with what Claude doesn't know.** Claude is already good at most programming tasks. The value of a skill is the delta — domain-specific knowledge, project conventions, opinionated workflows.

## References

- `plugins/plugin-authoring/skills/agent-skills/` — canonical skill authoring guide
- `plugins/plugin-authoring/skills/write-for-llms/` — example: domain knowledge skill
- `plugins/plugin-authoring/skills/create-agents/` — example: workflow skill
- Official Claude Code skills documentation: `code.claude.com/docs/skills` (fetch locally via `scripts/fetch-claude-code-docs.py`)
- Agent Skills open standard: `agentskills.io`
