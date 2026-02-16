# Subagent Quick Reference

## Frontmatter Template

```yaml
---
name: subagent-name
description: When to invoke. Include PROACTIVELY or Use when for auto-delegation.
tools: Read, Grep, Glob, Bash
disallowedTools: Delete
model: sonnet
permissionMode: default
skills: skill-name
# memory: project
# mcpServers:
#   server-name:
#     command: npx
#     args: ["-y", "@org/server-package"]
# maxTurns: 50
hooks:
  PreToolUse:
    - matcher: "ToolName"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---
```

## Tool Combinations

### Read-Only Analysis
```yaml
tools: Read, Grep, Glob, Bash
```
Best for: Code review, research, analysis, security audits

### Light Editing
```yaml
tools: Read, Edit, Grep, Glob
```
Best for: Bug fixes, refactoring, small modifications

### Full Development
```yaml
tools: Read, Write, Edit, Grep, Glob, Bash
```
Best for: Feature development, test creation, file generation

### Safe Refactoring
```yaml
tools: Read, Edit, Grep, Glob, Bash
disallowedTools: Delete, Write
```
Best for: Refactoring without creating/deleting files

## Description Patterns

### Proactive Invocation
```yaml
description: Expert code reviewer. Use PROACTIVELY after writing or modifying code.
```

### Conditional Invocation
```yaml
description: Debugging specialist. Use when encountering errors or unexpected behavior.
```

### Mandatory Invocation
```yaml
description: Security auditor. MUST BE USED before committing auth-related changes.
```

### Domain-Specific
```yaml
description: SQL query expert. Use for database queries, data analysis, and BigQuery operations.
```

## Model Selection

| Model | Speed | Cost | Use When |
|-------|-------|------|----------|
| `haiku` | Fastest | Lowest | Simple searches, file exploration, read-only |
| `sonnet` | Balanced | Medium | Most tasks (default) |
| `opus` | Slowest | Highest | Complex analysis, architecture decisions |
| `inherit` | Varies | Varies | Consistency with main conversation |

## Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Standard prompts |
| `acceptEdits` | Auto-accept file edits |
| `delegate` | Delegate to parent agent |
| `dontAsk` | Auto-deny prompts (allowed tools work) |
| `bypassPermissions` | Skip all checks (dangerous) |
| `plan` | Read-only exploration |

## Hook Patterns

### Validate Before Tool Use
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
```

### Run After Tool Use
```yaml
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
```

### Multiple Matchers
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-bash.sh"
    - matcher: "Edit"
      hooks:
        - type: command
          command: "./scripts/validate-edit.sh"
```

Hook exit codes:
- `0` - Continue normally
- `2` - Block operation (stderr message fed to Claude)

## System Prompt Templates

### Task-Based
```markdown
You are a [role] specializing in [domain].

When invoked:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Process:
- [Guideline 1]
- [Guideline 2]

For each [output]:
- [Requirement 1]
- [Requirement 2]
```

### Checklist-Based
```markdown
You are a [role] ensuring [standards].

When invoked:
1. [Initial action]
2. [Process step]
3. [Final action]

[Task] checklist:
- [Item 1]
- [Item 2]
- [Item 3]

Provide feedback by priority:
- Critical (must fix)
- Warnings (should fix)
- Suggestions (consider)

Include specific examples.
```

### Analysis-Based
```markdown
You are a [role] specializing in [analysis type].

When invoked:
1. Understand [requirement]
2. [Action step]
3. Analyze [subject]
4. Present findings

For each analysis:
- Explain approach
- Document assumptions
- Highlight findings
- Suggest next steps

Always [constraint].
```

## Common Workflow Patterns

### Git-Aware
```markdown
When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin [task]
```

### Test-Running
```markdown
When invoked:
1. Identify which tests to run based on changed files
2. Run the test suite
3. If tests pass, report success
4. If tests fail, analyze and fix
```

### Security-Focused
```markdown
Security checklist:
- Input validation (SQL injection, XSS, command injection)
- Authentication and authorization
- Secrets management (no hardcoded credentials)
- Data exposure (PII, sensitive data)
```

## File Locations

| Location | Scope | Priority |
|----------|-------|----------|
| `--agents` CLI flag | Session only | 1 (highest) |
| `.claude/agents/` | Project | 2 |
| `~/.claude/agents/` | User (all projects) | 3 |
| Plugin `agents/` | Where enabled | 4 (lowest) |

## Debugging Tips

### Subagent Not Triggering
1. Check description has clear trigger words
2. Add "PROACTIVELY" or "MUST BE USED"
3. Explicitly mention subagent in request
4. Use `/agents` to reload (or restart session)

### Wrong Tools Used
1. Specify exact tools in `tools` field
2. Use `disallowedTools` for denylist
3. Don't rely on inheritance if specific tools needed

### Poor Output Quality
1. Make system prompt more specific
2. Add checklists and structured guidance
3. Include examples in system prompt
4. Test with real tasks and iterate

### Hook Not Running
1. Verify script path is correct
2. Make script executable (`chmod +x`)
3. Check matcher regex matches tool name
4. Test script manually with JSON input

### Permission Issues
1. Check `permissionMode` setting
2. Verify parent permissions
3. Background subagents auto-deny unapproved actions

## CLI JSON Format

```bash
claude --agents '{
  "agent-name": {
    "description": "When to use",
    "prompt": "System prompt content",
    "tools": ["Read", "Grep", "Glob"],
    "disallowedTools": ["Delete"],
    "model": "sonnet",
    "permissionMode": "default"
  }
}'
```
