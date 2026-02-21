---
title: Subagents
description: "Subagents isolate concerns. Each one handles a single responsibility with scoped tools and a focused system prompt."
---

# Subagents

> Subagents isolate concerns. Each one handles a single responsibility with scoped tools and a focused system prompt. The scope constraint is what produces better output.

## What It Is

Subagents run in isolated context with constrained tools, specific system prompts, and optional skill loading. They delegate focused work from the main conversation — an architect subagent thinks about structure, a security subagent scans for vulnerabilities, a reviewer subagent reads code. Each operates within its defined scope.

Subagents are defined as markdown files with YAML frontmatter (the spec) and a markdown body (the system prompt). Each runs in its own context window, receives only its system prompt plus basic environment details (working directory), and returns results to the caller when done.

**Key constraints:**

- Subagents **do not see the main conversation**. All necessary context must be provided in the delegation prompt.
- Subagents **cannot spawn other subagents**. If a workflow requires nested delegation, chain subagents from the main conversation or use skills instead.
- Subagents **do not inherit skills** from the parent conversation. Skills must be listed explicitly in the `skills` frontmatter field, and [their full content is injected at startup — not progressively disclosed](https://code.claude.com/docs/en/sub-agents#preload-skills-into-subagents ).

## When to Use (and When Not To)

Subagents are the right choice when a task benefits from isolated context, constrained tools, and a focused system prompt. They earn their existence through repeated delegation — if you'd only use one once, it's not worth the definition.

For cross-primitive comparison (when to use a Subagent vs. a Skill, Hook, Connector, or LSP Server), see the [Primitives Guide](_GUIDE.md).

## Built-in Subagents

Claude Code includes built-in subagents that are automatically available. Each inherits the parent conversation's permissions with additional tool restrictions.

| Agent                 | Model   | Tools                      | Purpose                                                                                            |
| --------------------- | ------- | -------------------------- | -------------------------------------------------------------------------------------------------- |
| **Explore**           | Haiku   | Read-only (no Write, Edit) | Fast codebase search and analysis. Claude specifies thoroughness: quick, medium, or very thorough. |
| **Plan**              | Inherit | Read-only (no Write, Edit) | Research during plan mode. Gathers context before presenting a plan.                               |
| **general-purpose**   | Inherit | All tools                  | Complex multi-step tasks requiring both exploration and modification.                              |
| **Bash**              | Inherit | —                          | Terminal commands in a separate context.                                                           |
| **Claude Code Guide** | Haiku   | —                          | Answering questions about Claude Code features.                                                    |

You cannot modify built-in subagents, but you can [disable them](#disabling-subagents) or create custom subagents that handle the same tasks differently.

## Roles Constrain Attention

Role scoping produces better output when it narrows the problem space. An architect subagent works because it deliberately ignores implementation detail to focus on structure. A security reviewer works because it evaluates only threat surfaces, not feature completeness.

**The principle: roles must earn their existence by producing meaningfully different output than an unscoped subagent would.**

Role definitions become harmful when they add ceremony without narrowing focus, or when subagents generate discussion for the appearance of rigor rather than producing better output. Agent Teams — where a lead coordinates specialized teammates working in parallel — are legitimate orchestration, not simulation. The question is always whether the structure produces better work, not whether it looks impressive.

## How It Works

### Subagent Anatomy

A subagent is a markdown file with YAML frontmatter and a system prompt body:

```yaml
---
name: code-reviewer
description: Reviews code changes for correctness and style. Use proactively after code modifications.
model: sonnet
tools: Read, Grep, Glob
---
You are a code reviewer. Focus on correctness, clarity, and adherence
to project conventions. Never suggest implementation changes — only
identify problems and explain why they matter.
```

**Frontmatter fields:**

| Field             | Required | Description                                                                                                |
| ----------------- | -------- | ---------------------------------------------------------------------------------------------------------- |
| `name`            | Yes      | Subagent identifier. Lowercase letters and hyphens.                                                        |
| `description`     | Yes      | What the subagent does and when to invoke it. Use [proactive trigger words](#the-description-field).       |
| `tools`           | No       | [Tool access](#tool-control). Comma-separated allowlist. Inherits all tools if omitted.                    |
| `disallowedTools` | No       | Tools to deny, removed from inherited or specified list.                                                   |
| `model`           | No       | `sonnet`, `opus`, `haiku`, or `inherit` (default).                                                         |
| `color`           | No       | Terminal background color for visual distinction (`blue`, `cyan`, `green`, `yellow`, `magenta`, `red`).    |
| `permissionMode`  | No       | [Permission mode](#permission-modes): `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, or `plan`. |
| `skills`          | No       | [Skills preloaded](#preloading-skills) into the subagent's context at startup.                             |
| `hooks`           | No       | [Hooks](#hooks-in-subagents) scoped to this subagent's lifecycle.                                          |
| `mcpServers`      | No       | [MCP servers](#mcp-servers) available to this subagent.                                                    |
| `maxTurns`        | No       | Maximum agentic turns before the subagent must stop. Use for long-running or potentially unbounded tasks.  |
| `memory`          | No       | [Persistent memory](#persistent-memory) scope: `user`, `project`, or `local`.                              |

### The Description Field

The `description` field is how Claude decides when to delegate. Vague descriptions mean Claude won't use your subagent. Include:

- **What** the subagent does
- **When** to invoke it (trigger conditions)
- **Proactive trigger words**: `proactively`, `use when`, `must be used`, `immediately`, `use for`

For maximum clarity, include `<example>` blocks in the description showing context, user input, and expected delegation:

```yaml
description: >
  Expert code reviewer. PROACTIVELY reviews code for quality, security,
  and maintainability. Use immediately after writing or modifying code.

  <example>
  context: User just finished implementing a feature
  user: Review this code for any issues
  assistant: [delegates to code-reviewer subagent]
  <commentary>The subagent should be invoked whenever code review is requested or after significant code changes.</commentary>
  </example>
```

### Tool Control

Grant minimal access. A reviewer doesn't need Write. A researcher doesn't need Bash.

**Allowlist** (only these tools available):

```yaml
tools: Read, Grep, Glob
```

**Denylist** (everything except these):

```yaml
disallowedTools: Write, Edit, Bash
```

**Both fields work together.** If `tools` specifies an allowlist, `disallowedTools` removes from that list. If `tools` is omitted (inherit all), `disallowedTools` removes from the inherited set.

**Restricting subagent spawning** — for agents running as the main thread with `claude --agent`, use `Task(agent_type)` syntax to control which subagents it can spawn:

```yaml
tools: Task(worker, researcher), Read, Bash
```

This is an allowlist: only `worker` and `researcher` subagents can be spawned. To block specific agents while allowing all others, use `permissions.deny` instead. Note: this only applies to agents running as the main thread — regular subagents cannot spawn other subagents regardless.

**Available internal tools:** `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Bash`, `Delete`. MCP tools use the `mcp__<server>__<tool>` format.

### Permission Modes

| Mode                | Behavior                                                             | Use When                       |
| ------------------- | -------------------------------------------------------------------- | ------------------------------ |
| `default`           | Asks for permission on sensitive operations                          | Standard work                  |
| `acceptEdits`       | Auto-approves file edits, asks for other actions                     | Trusted editing tasks          |
| `plan`              | Read-only, no modifications                                          | Research and planning          |
| `dontAsk`           | Auto-denies permission prompts (explicitly allowed tools still work) | Background tasks               |
| `bypassPermissions` | No permission checks                                                 | **Only with PreToolUse hooks** |

**Inheritance rule:** If the parent uses `bypassPermissions`, this takes precedence and cannot be overridden by a subagent's `permissionMode`.

### Model Selection

| Model                 | When to Use                                                          |
| --------------------- | -------------------------------------------------------------------- |
| **inherit** (default) | Use parent's model. The safe default.                                |
| **sonnet**            | Fast, capable. Good for most focused tasks.                          |
| **opus**              | Maximum capability. Complex reasoning, architectural decisions.      |
| **haiku**             | Fast and cheap. Simple, well-scoped tasks like search or formatting. |

### Persistent Memory

The `memory` field gives a subagent a persistent directory that survives across conversations. The subagent builds up knowledge over time — codebase patterns, debugging insights, architectural decisions.

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---
You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

**Scopes:**

| Scope     | Location                             | Use When                                                  |
| --------- | ------------------------------------ | --------------------------------------------------------- |
| `user`    | `~/.claude/agent-memory/<name>/`     | Learnings that apply across all projects                  |
| `project` | `.claude/agent-memory/<name>/`       | Project-specific knowledge, shareable via version control |
| `local`   | `.claude/agent-memory-local/<name>/` | Project-specific, not checked into version control        |

**Behavior when enabled:**

- The system prompt includes instructions for reading/writing to the memory directory.
- The first 200 lines of `MEMORY.md` in the memory directory are included in the system prompt. If `MEMORY.md` exceeds 200 lines, the subagent is instructed to curate it.
- `Read`, `Write`, and `Edit` tools are automatically enabled so the subagent can manage its memory files.

**Tips:**

- `user` is the recommended default scope.
- Ask the subagent to consult its memory before starting work: "Review this PR, and check your memory for patterns you've seen before."
- Ask the subagent to update its memory after completing a task to build institutional knowledge.
- Include memory instructions directly in the system prompt so it proactively maintains its knowledge base.

### Preloading Skills

Use the `skills` field to inject skill content into a subagent's context at startup. The full content is injected — not just made available for invocation.

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---
Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

**Don't repeat skill content in the system prompt.** Preload the skill and let it do its job. This keeps the system prompt focused on the subagent's role and constraints.

This is the inverse of `context: fork` in a skill definition. With `skills` in a subagent, the subagent controls the system prompt and loads skill content. With `context: fork` on a skill, the skill's content is injected into a specified subagent. Both use the same underlying system.

### Hooks in Subagents

Subagents support hooks in two ways: scoped to the subagent's lifecycle (in frontmatter) and scoped to the project (in `settings.json`).

**Frontmatter hooks** — run only while the subagent is active:

```yaml
---
name: safe-editor
description: Edits code with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

Supported events in frontmatter: `PreToolUse` (before tool use, can block with exit code 2), `PostToolUse` (after tool use), `Stop` (when subagent finishes — automatically converted to `SubagentStop` at runtime).

**Project-level hooks** — defined in `settings.json`, fire in the main session:

| Event           | Matcher Input   | When It Fires                    |
| --------------- | --------------- | -------------------------------- |
| `SubagentStart` | Agent type name | When a subagent begins execution |
| `SubagentStop`  | Agent type name | When a subagent completes        |

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [{ "type": "command", "command": "./scripts/setup-db-connection.sh" }]
      }
    ]
  }
}
```

**Hook I/O:** Hook commands receive JSON via stdin with fields including `hook_event_name`, `tool_name`, `tool_input`, `session_id`, `cwd`, `permission_mode`, and `stop_hook_active`. For `PreToolUse`, exit code 0 continues, exit code 2 blocks the operation (stderr message feeds back to the subagent). The `stop_hook_active` field guards against infinite loops in Stop hooks.

### MCP Servers

Subagents can access MCP servers configured at the project or user level. Reference an already-configured server by name, or define one inline:

```yaml
---
name: data-analyst
mcpServers:
  postgres:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-postgres"]
    env:
      DATABASE_URL: "postgresql://localhost:5432/mydb"
---
```

Restrict specific MCP tools using `mcp__<server>__<tool>` format in the `tools` or `disallowedTools` fields.

**Note:** MCP tools are unavailable in background subagents.

### Execution Modes

**Foreground** (default) — the subagent runs, the main conversation waits, results return to context. Permission prompts and clarifying questions pass through to the user. Suitable for most tasks.

**Background** (`run_in_background: true`) — the subagent runs independently while the main conversation continues. Before launching, Claude Code prompts for any tool permissions the subagent will need upfront. Once running:

- The subagent inherits pre-approved permissions and auto-denies anything not pre-approved.
- If the subagent needs to ask clarifying questions, the tool call fails but the subagent continues.
- MCP tools are not available.
- Context compaction can introduce artifacts in long-running background agents.

**Ctrl+B** backgrounds a running foreground task.

If a background subagent fails due to missing permissions, you can [resume it](#resuming-subagents) in the foreground to retry with interactive prompts.

To disable all background task functionality, set `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`.

### Resuming Subagents

Each subagent invocation creates a new instance with fresh context. To continue an existing subagent's work instead of starting over, ask Claude to resume it.

Resumed subagents retain their full conversation history — all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped.

When a subagent completes, Claude receives its agent ID. To resume:

```
Use the code-reviewer agent to review the auth module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

**Transcript persistence:** Subagent transcripts are stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`. Transcripts persist independently of the main conversation — main conversation compaction does not affect them. Transcripts are cleaned up based on the `cleanupPeriodDays` setting (default: 30 days).

### Context Management

Subagents support automatic compaction using the same logic as the main conversation. By default, auto-compaction triggers at approximately 95% capacity.

To trigger compaction earlier, set `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` to a lower percentage (e.g., `50`).

**Compaction artifact template** for long-running agents — when compaction occurs, structure the summary to preserve state:

```markdown
## Compaction Summary

**Goal:** [original objective]
**Approach:** [strategy being followed]
**Completed:** [what's done]
**Active Blockers:** [current obstacles]
**Next Steps:** [immediate actions remaining]
```

## Configuration

### File Locations and Scope Priority

When multiple subagents share the same name, the higher-priority location wins:

| Priority    | Location                     | Scope                   | How to Create                          |
| ----------- | ---------------------------- | ----------------------- | -------------------------------------- |
| 1 (highest) | `--agents` CLI flag          | Current session only    | Pass JSON when launching Claude Code   |
| 2           | `.claude/agents/<name>.md`   | Current project         | Interactive (`/agents`) or manual file |
| 3           | `~/.claude/agents/<name>.md` | All your projects       | Interactive (`/agents`) or manual file |
| 4 (lowest)  | `<plugin>/agents/<name>.md`  | Where plugin is enabled | Installed with plugins                 |

**Project subagents** (`.claude/agents/`) are ideal for team-shared agents. Check them into version control.

**User subagents** (`~/.claude/agents/`) are personal agents available in all projects.

### The /agents Command

Run `/agents` to interactively manage subagents:

- View all available subagents (built-in, user, project, plugin)
- Create new subagents with guided setup or Claude generation
- Edit existing subagent configuration and tool access
- Delete custom subagents
- See which subagents are active when duplicates exist

Subagents created via `/agents` are available immediately without restarting. Manually created files require a session restart or `/agents` to reload.

### CLI JSON Format

The `--agents` flag passes subagent definitions as JSON for a single session — useful for testing or automation:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

The JSON accepts the same fields as file-based frontmatter: `description`, `prompt` (equivalent to the markdown body), `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, and `memory`.

### Disabling Subagents

Prevent Claude from using specific subagents by adding `Task(subagent-name)` to the `deny` array in settings:

```json
{
  "permissions": {
    "deny": ["Task(Explore)", "Task(my-custom-agent)"]
  }
}
```

Or via CLI: `claude --disallowedTools "Task(Explore)"`. Works for both built-in and custom subagents.

## Context Engineering

Subagents exist to isolate context. Understanding how context flows — and where it goes wrong — is the difference between subagents that produce good work and subagents that degrade into noise.

### The Context Cost Pyramid

Errors compound upstream. A bad line of code is localized — fix the line, problem solved. A bad line in a plan cascades into hundreds of implementation errors. A bad line in research propagates into thousands of downstream failures across every plan and implementation that relies on it.

```
              ▲
             /|\         Research errors → thousands of failures
            / | \
           /  |  \       Plan errors → hundreds of failures
          /   |   \
         /    |    \     Code errors → localized failures
        /_____|_____\
```

**Implication for subagents:** Subagents doing research need the most careful context management. An architect subagent that hallucinates a constraint poisons every implementation decision downstream. A code-formatting subagent that misses a style rule causes one bad file.

### Utilization Targets

Target **40-60% context utilization** for optimal subagent performance. The final 20% of context capacity is a degradation zone — the subagent starts losing coherence, forgetting earlier instructions, and producing lower-quality output.

For codebases over 100k LOC, use subagents to keep the main conversation clean. Feed subagents a focused specification (~5,000 token markdown spec) rather than allowing them to explore the entire repository.

### Compaction Artifacts

Long-running subagents will eventually trigger auto-compaction. When this happens, prior context is summarized. To minimize information loss, instruct subagents to maintain running state in the compaction-friendly format shown in [Context Management](#context-management).

### Multi-Claude Workflows

Subagents power several multi-instance patterns:

**Write + Review** — one subagent implements, another reviews. The reviewer gets only Read tools and cannot modify the implementation. Quality gate without blurred responsibility.

**Parallel Features** — use separate `git worktree` directories so multiple subagents can work on independent features without file conflicts. Each subagent operates in its own worktree, merges happen after completion.

**Fan-out Analysis** — spawn multiple subagents, each analyzing one component or module. Collect results and synthesize. Best when the analyses are truly independent.

**Headless orchestration** — `claude -p` runs Claude Code non-interactively. Combine with `--output-format stream-json`, `--allowedTools`, and `--agents` for scripted multi-subagent pipelines. Use `--continue` or `--resume <session-id>` for conversation continuity across invocations.

## Coordination

### Escalation Triggers

Flag for Code Actual when:

- New pattern not in existing ADRs
- Significant tech choice (hard to reverse)
- Cross-cutting concerns (auth, logging, observability)
- Scope creep or conflicting requirements
- "I don't know how this should work"

### Large Operations

Operations with **10+ subagent spawns** require a persistent plan file:

**File:** `plans/{operation-name}.md`

**Required sections:**

- Mission parameters (total subagents, batches, rounds)
- Current progress tracker (checkboxes or status table)
- Batch assignments with completion status
- Quarantine/exception list

**Why:** Without a readable plan file, Code Actual cannot track progress or understand remaining work. Rounds get skipped unintentionally, state becomes unclear, and coordination fails.

**Update cadence:** After each batch completes or when status changes.

## Patterns

### Lead + Specialist Teams

A lead subagent coordinates specialized teammates working in parallel. Each specialist has its own tools and skills. The lead delegates, collects results, and synthesizes. Legitimate orchestration, not simulation.

### Read-Only Reviewers

Review subagents get only Read, Grep, Glob — never Write or Edit. A reviewer that can modify code blurs the boundary between review and implementation.

### Skill-Loaded Specialists

Subagents can preload skills via the `skills` frontmatter field. The full skill content is injected at startup, giving the subagent domain expertise without reproducing it in the system prompt. Example: a testing subagent preloads the TDD skill.

### Scoped Hooks on Subagents

Subagents can define hooks in their frontmatter that only apply during the subagent's lifecycle. `Stop` hooks on subagents automatically become `SubagentStop` hooks. Use this for quality gates: the subagent can't finish until its hook-checked conditions pass.

### Chain Subagents

For multi-step workflows, use subagents in sequence from the main conversation. Each subagent completes its task and returns results to Claude, which passes relevant context to the next subagent:

```
Use the code-reviewer agent to find performance issues,
then use the optimizer agent to fix them
```

This works because the main conversation acts as the orchestrator — it sees all results and can provide appropriate context to each subsequent subagent.

### Isolate High-Volume Operations

One of the most effective uses for subagents is isolating operations that produce large output. Running tests, fetching documentation, or processing log files can consume significant main-conversation context. Delegate to a subagent and only the relevant summary returns:

```
Use a subagent to run the test suite and report only failing tests with error messages
```

### Parallel Research

For independent investigations, spawn multiple subagents simultaneously:

```
Research the authentication, database, and API modules in parallel using separate subagents
```

Each subagent explores independently, then Claude synthesizes. Works best when the research paths don't depend on each other. **Caution:** when subagents complete, their results return to the main conversation — many detailed results can consume significant context.

### Testing Skills with Subagents

Subagents serve as test subjects for validating skill effectiveness using a RED-GREEN-REFACTOR cycle:

1. **RED** — Run a scenario without the skill loaded. Watch the subagent fail or produce suboptimal output. This establishes the baseline.
2. **GREEN** — Load the skill and run the same scenario. The subagent should now comply with the skill's guidance.
3. **REFACTOR** — Apply pressure scenarios (time pressure, sunk cost, authority) and watch for rationalizations. Add explicit counters for each rationalization found.

**Only test skills that enforce discipline** — skills with compliance costs that a subagent might rationalize away. Don't test pure reference skills.

**Pressure scenarios** combine 3+ pressures (time, sunk cost, authority, exhaustion, economic, social) to expose the subagent's rationalizations for bypassing skill guidance.

**Meta-testing technique:** After a subagent violates a skill's guidance, ask it: "How could the skill have been written differently to make it crystal clear?" Three outcomes reveal different problems:

- "The skill was clear, I chose to ignore it" → foundational principle problem
- "The skill should have said X" → documentation gap
- "I didn't see section Y" → organizational problem

## Anti-Patterns

| Pattern                               | Problem                                      | Fix                                                                             |
| ------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------- |
| **Swiss-army subagent**               | Too many tools, too broad a scope            | One subagent = one responsibility. Split concerns.                              |
| **Write tools on reviewer**           | Reviewer modifies code, blurs responsibility | Read-only tool access for reviewers                                             |
| **bypassPermissions without hooks**   | No safety net on unrestricted access         | Always pair with PreToolUse hooks                                               |
| **Single-use subagent**               | Overhead of definition for one invocation    | Use Task tool directly                                                          |
| **Vague description**                 | Claude doesn't know when to delegate to it   | Use proactive trigger words and `<example>` blocks                              |
| **Giant system prompt**               | Context bloat, diluted focus                 | Use skills for knowledge; keep system prompt focused on role and constraints    |
| **Expecting conversation context**    | Subagents don't see the main conversation    | Provide all necessary context in the delegation prompt                          |
| **No output format**                  | Subagent returns unstructured results        | Specify output format in system prompt (checklist, report, structured sections) |
| **Spawning subagents from subagents** | Subagents cannot spawn other subagents       | Chain from main conversation or use skills                                      |

## Examples

### Code Reviewer (Read-Only)

Demonstrates minimal tool access and structured output. The subagent can analyze but never modify.

```yaml
---
name: code-reviewer
description: >
  Expert code review specialist. PROACTIVELY reviews code for quality,
  security, and maintainability. Use immediately after writing or
  modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality
and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger (Diagnostic + Fix)

Demonstrates full development tools with a structured diagnostic workflow.

```yaml
---
name: debugger
description: >
  Debugging specialist for errors, test failures, and unexpected behavior.
  Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Database Reader (Hooks as Guardrails)

Demonstrates `PreToolUse` hooks for conditional validation — the subagent has Bash access but is mechanically restricted to read-only SQL.

```yaml
---
name: db-reader
description: >
  Execute read-only database queries. Use when analyzing data or
  generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries
to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify
schema, explain that you only have read access.
```

The companion validation script:

```bash
#!/bin/bash
# ./scripts/validate-readonly-query.sh
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

### Data Scientist (Domain Specialist)

Demonstrates domain-specific subagents with explicit model selection for analytical capability.

```yaml
---
name: data-scientist
description: >
  Data analysis expert for SQL queries, BigQuery operations, and data
  insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data
```

## Agent Teams

Agent teams coordinate multiple independent Claude Code instances working together. Unlike subagents (which run within a single session and report back), teammates are separate sessions with their own context windows that communicate with each other via a shared task list and messaging system.

|                   | Subagents                                      | Agent Teams                                         |
| ----------------- | ---------------------------------------------- | --------------------------------------------------- |
| **Context**       | Own context window; results return to caller   | Own context window; fully independent               |
| **Communication** | Report results back to caller only             | Teammates message each other directly               |
| **Coordination**  | Caller manages all work                        | Shared task list with self-coordination             |
| **Best for**      | Focused tasks where only the result matters    | Complex work requiring discussion and collaboration |
| **Token cost**    | Lower: results summarized back to main context | Higher: each teammate is a separate Claude instance |

**Status:** Agent teams are experimental and disabled by default. Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings or environment.

**When to use teams over subagents:**

- Research and review needing multiple simultaneous perspectives
- Debugging with competing hypotheses tested in parallel
- Cross-layer coordination (frontend, backend, tests each owned separately)
- Work where teammates need to challenge each other's findings

**When to stick with subagents:** Sequential tasks, same-file edits, work with many dependencies, or when coordination overhead isn't worth the parallelism.

See [official agent teams documentation](https://code.claude.com/docs/en/agent-teams) for full configuration, display modes, and team management.

## Our Opinions

- **One subagent = one responsibility.** If you can't name the responsibility in two words, the scope is wrong.
- **Start with skills.** Only create a subagent when the focus genuinely improves output. Many tasks work fine with a skill loaded into the main conversation.
- **Read-only for review.** Never give a reviewer write access. Review and implementation are separate concerns.
- **Every subagent using `bypassPermissions` must have PreToolUse hooks.** No exceptions. Unrestricted access without guardrails is how incidents happen.
- **Subagents load skills at startup — use this.** Don't repeat skill content in the system prompt. Preload the skill and let it do its job.
- **Roles justify themselves through output quality, not by existing.** If a subagent doesn't produce meaningfully different output than an unscoped subagent, it doesn't need to exist.
- **Memory is underused.** Most subagents that run repeatedly would benefit from `memory: user`. Let them build institutional knowledge across conversations.
- **Context is the scarce resource.** Design subagents to be context-efficient — focused system prompts, skills for knowledge, structured output formats. Target 40-60% context utilization for optimal performance.
- **Intellectual weight lives in skills; subagents provide scaffolding.** Skills carry domain knowledge. Subagents are the delivery mechanism that applies it with focus and tool constraints.

## References

- [Official Claude Code subagents documentation](https://code.claude.com/docs/en/sub-agents)
- [Official agent teams documentation](https://code.claude.com/docs/en/agent-teams)
- [Official headless/Agent SDK documentation](https://code.claude.com/docs/en/headless)
- [Doctrine](../development/DOCTRINE.md) § The Five Primitives, § On Roles
- [ADR-0004: Five Primitives Model](../decisions/0004-six-primitives-model.md) — naming history (Agents → Subagents)
- [ADR-0010: Agent-Per-Stage Pattern](../decisions/0010-agent-per-stage-pattern.md) — deprecated but instructive
- Fetch platform docs locally: `python scripts/fetch_claude_code_docs.py --only sub-agents agent-teams headless`
