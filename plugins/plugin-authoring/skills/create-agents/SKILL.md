---
name: create-agents
description: Guide for creating effective subagents. Use when users want to create, update, or understand subagents that delegate specialized tasks with custom context, tools, and system prompts. Triggers on "create an agent", "make a subagent", "agent configuration", "what tools should my agent have".
author: witoldwozniak
license: Hippocratic-3.0
---

# Creating Subagents

**Key constraint:** Subagents receive only their system prompt plus basic environment details (working directory), not the full Claude Code system prompt. Subagents cannot spawn other subagents.

### Skills vs Subagents

| Skills | Subagents |
|--------|-----------|
| HOW to do something | WHO should do it |
| Workflows, procedures, tools | Specialized AI personas |
| Run in main conversation context | Run in isolated context |
| Can be loaded into subagents | Cannot spawn other subagents |

Use **skills** for: Reusable workflows, tool integrations, domain knowledge
Use **subagents** for: Task delegation, context management, specialized review/analysis

### Built-in Subagents

Claude Code includes built-in subagents used automatically:

| Subagent | Model | Tools | Purpose |
|----------|-------|-------|---------|
| **Explore** | Haiku | Read-only | Fast codebase search and analysis |
| **Plan** | Inherit | Read-only | Research for plan mode |
| **general-purpose** | Inherit | All | Complex multi-step tasks |

## Subagent Anatomy

Subagent files use YAML frontmatter for configuration, followed by the system prompt in Markdown:

```markdown
---
name: code-reviewer
description: Reviews code for quality. Use PROACTIVELY after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | 3-50 chars, lowercase/numbers/hyphens, alphanumeric start/end |
| `description` | Yes | When Claude should delegate (include trigger words and examples) |
| `tools` | No | Tools to allow (inherits all if omitted) |
| `disallowedTools` | No | Tools to deny (removed from inherited/specified list) |
| `model` | No | `sonnet` / `opus` / `haiku` / `inherit` (default: `inherit`) |
| `permissionMode` | No | `default` / `acceptEdits` / `delegate` / `dontAsk` / `bypassPermissions` / `plan` |
| `skills` | No | Skills to load into subagent's context at startup |
| `hooks` | No | Lifecycle hooks scoped to this subagent |
| `memory` | No | Memory scope: `project` / `user` / `none` (default: `none`) |
| `mcpServers` | No | MCP server configurations available to this subagent |
| `maxTurns` | No | Maximum agentic turns before stopping (positive integer) |

#### Description Field Format

The `description` field should include trigger conditions and concrete examples:

```markdown
description: |
  Reviews code for quality, security, and best practices. Use PROACTIVELY after code changes.

  <example>
  Context: User just modified authentication logic
  user: "I've updated the login function"
  assistant: "Let me review that with the code-reviewer subagent"
  <commentary>
  This agent should be triggered automatically after code modifications
  </commentary>
  </example>
```

Key elements:
- Clear trigger conditions (when Claude should delegate)
- Trigger words: "PROACTIVELY", "Use when", "MUST BE USED"
- Example blocks showing context, user input, and expected assistant behavior

### Tool Control Patterns

**Allowlist** - Specify only permitted tools:
```yaml
tools: Read, Grep, Glob, Bash
```

**Denylist** - Remove specific tools from inherited set:
```yaml
disallowedTools: Write, Edit, Delete
```

**Combined** - Allow some, deny others:
```yaml
tools: Read, Write, Edit, Bash
disallowedTools: Delete
```

### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Standard permission checking with prompts |
| `acceptEdits` | Auto-accept file edits |
| `delegate` | Delegate permission decisions to the parent agent |
| `dontAsk` | Auto-deny permission prompts (allowed tools still work) |
| `bypassPermissions` | Skip all permission checks (use with caution) |
| `plan` | Plan mode (read-only exploration) |

If parent uses `bypassPermissions`, this takes precedence and cannot be overridden.

### Memory

Subagents can persist and recall information across sessions using the `memory` field:

| Scope | Behavior |
|-------|----------|
| `none` | No memory (default) — stateless across sessions |
| `project` | Remembers context scoped to the current project |
| `user` | Remembers context scoped to the user across all projects |

```yaml
memory: project
```

### MCP Servers

Subagents can access MCP servers configured inline in frontmatter:

```yaml
mcpServers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_TOKEN: "${GITHUB_TOKEN}"
```

MCP tools are unavailable in background subagents. Use `mcp__<server>__<tool>` format in `tools` to restrict which MCP tools the subagent can access.

### Turn Limits

Set `maxTurns` to cap how many agentic turns a subagent can take before stopping:

```yaml
maxTurns: 50
```

Use for long-running or potentially unbounded tasks to prevent runaway execution. The subagent stops gracefully when the limit is reached.

### Model Selection

| Model | Use When |
|-------|----------|
| `inherit` | Default - uses same model as main conversation |
| `sonnet` | Balanced reasoning and speed |
| `opus` | Complex analysis, architecture decisions |
| `haiku` | Fast searches, simple read-only operations |

### Hooks

Subagents can define hooks that run during their lifecycle:

```yaml
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-query.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

**Hook events in frontmatter:**
- `PreToolUse` - Before subagent uses a tool (matcher: tool name)
- `PostToolUse` - After subagent uses a tool (matcher: tool name)
- `Stop` - When subagent finishes

Hook commands receive JSON via stdin with tool input. Exit codes:
- `0` - Continue normally
- `2` - Block the operation (error message via stderr fed back to Claude)

**Project-level hooks** in `settings.json` respond to subagent lifecycle:
- `SubagentStart` - When subagent begins (matcher: agent name)
- `SubagentStop` - When subagent completes (matcher: agent name)

## Subagent Scope & Priority

Store subagents in different locations depending on scope. When names conflict, higher priority wins:

| Priority | Location | Scope | How to create |
|----------|----------|-------|---------------|
| 1 (highest) | `--agents` CLI flag | Current session | JSON when launching |
| 2 | `.claude/agents/` | Current project | `/agents` or manual |
| 3 | `~/.claude/agents/` | All your projects | `/agents` or manual |
| 4 (lowest) | Plugin `agents/` dir | Where plugin enabled | Installed with plugins |

**Project subagents** - Check into version control for team collaboration.
**User subagents** - Personal subagents available everywhere.
**CLI subagents** - Temporary, not saved to disk.

## Execution Modes

### Foreground vs Background

- **Foreground** - Blocks main conversation. Permission prompts pass through to user.
- **Background** - Runs concurrently. Auto-denies unapproved permissions. MCP tools unavailable.

Press **Ctrl+B** to background a running task. Ask Claude to "run this in the background."

### Compaction Artifacts for Long-Running Agents

WHEN a subagent approaches context limits, structure compaction artifacts with: current goal statement, chosen approach rationale, completed steps summary, active blockers, next immediate steps. Use markdown files or commit messages as persistent state. See [context-engineering.md](references/context-engineering.md) for templates.

### Resuming Subagents

Each invocation creates fresh context. To continue existing work:

```
Use the code-reviewer subagent to review auth module
[Agent completes]

Continue that code review and analyze authorization logic
[Claude resumes with full context from previous conversation]
```

Subagent transcripts persist at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`.

## Creation Workflow

### Step 1: Use /agents Command (Recommended)

The `/agents` command provides interactive subagent management:
- View all subagents (built-in, user, project, plugin)
- Create new subagents with guided setup or Claude generation
- Edit existing configuration and tool access
- Delete custom subagents

### Step 2: Understand the Use Case

Ask clarifying questions (1-2 per message):
- "What specific task should this subagent handle?"
- "When should Claude automatically use it?"
- "What does success look like?"
- "Can you give usage examples?"

### Step 3: Design the Subagent

Determine:
1. **Name** - Descriptive, lowercase with hyphens
2. **Description** - Include trigger words ("PROACTIVELY", "Use when", "MUST BE USED")
3. **Tools** - Minimal set needed for the task
4. **Model** - Match to task complexity
5. **System prompt** - Define role, process, constraints

### Step 4: Write System Prompt

Structure:
1. **Role definition** - "You are a [role] specializing in [domain]"
2. **When invoked** - Clear steps to take immediately
3. **Process/Checklist** - Criteria to follow
4. **Output format** - How to present results
5. **Constraints** - What to avoid or prioritize

### Step 5: Generate the File

Create at appropriate location:
- Project: `.claude/agents/<name>.md`
- User: `~/.claude/agents/<name>.md`

**Note:** Subagents load at session start. Use `/agents` to load immediately without restart.

### Step 6: Verify and Iterate

1. Confirm file created successfully
2. Show user the complete definition
3. Test with real tasks
4. Iterate based on results

## Testing Checklist

- [ ] Agent triggers automatically on matching tasks
- [ ] Agent accepts explicit invocation ("Use the [name] subagent to...")
- [ ] System prompt steps execute in order
- [ ] Output format is correct and complete
- [ ] Tool restrictions work as intended
- [ ] Permission mode behaves correctly

## Core Principles

### Focus Over Flexibility

Create subagents with single, clear responsibilities.

**Good:** `test-runner` - Runs tests and fixes failures
**Bad:** `code-helper` - Does everything code-related

### Proactive Descriptions

Include explicit triggers in the `description` field:

**Good:** "Expert code reviewer. Use PROACTIVELY after writing or modifying code."
**Bad:** "Reviews code for quality and security."

### Minimal Tool Access

Grant only necessary tools. This improves security and focus.

**Good:** Code reviewer gets `Read, Grep, Glob, Bash` (read-only)
**Bad:** Code reviewer gets `Edit, Write, Delete` (unnecessary)

### Context Cost Awareness

Errors cascade with increasing severity upstream: a bad code line is a localized problem, a bad plan line causes hundreds of cascading errors, a bad research line causes thousands of downstream failures. Target 40-60% context utilization — beyond this, model recall degrades. See [context-engineering.md](references/context-engineering.md) for the cost pyramid and compaction patterns.

### Isolate High-Volume Operations

Delegate operations producing large output (tests, logs, docs) to keep main context clean.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Swiss-army agent** | "code-helper" does everything | One agent = one responsibility |
| **Write tools on read-only agents** | Review agent with Edit/Write can modify code | Use `disallowedTools: Write, Edit, Delete` |
| **bypassPermissions without hooks** | No safety net for destructive actions | Add PreToolUse hooks for validation |
| **Expecting conversation context** | Agent asks "what file?" when user mentioned it | Pass explicit context in the Task prompt |
| **Single-use agents** | Creating agent for one-time task | Just do the task directly |
| **Vague descriptions** | "Helps with code" never triggers | Include PROACTIVELY, Use when, specific scenarios |
| **Giant system prompts** | 1000+ word prompts waste tokens | Keep to essential role + process + constraints |
| **No output format** | Agent returns unstructured text | Define sections, headings, expected content |

## Disabling Subagents

Add to `deny` array in settings using `Task(subagent-name)` format:

```json
{
  "permissions": {
    "deny": ["Task(Explore)", "Task(my-custom-agent)"]
  }
}
```

Or via CLI: `claude --disallowedTools "Task(Explore)"`

## References

- `references/example-subagents.md` - Complete working examples including hooks
- `references/quick-reference.md` - Tool combinations, templates, debugging tips
- `references/context-engineering.md` - Context cost pyramid, compaction artifacts, multi-Claude workflows

## Scripts

- `scripts/init_subagent.py` - Initialize new subagent with template
- `scripts/validate_subagent.py` - Validate subagent format and content
