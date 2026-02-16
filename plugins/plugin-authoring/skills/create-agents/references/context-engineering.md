# Context Engineering for Subagents

Patterns for managing context as a finite resource in subagent design and long-running agent workflows.

## Context Cost Pyramid

Errors compound with increasing severity upstream:

| Error Location | Downstream Impact |
|----------------|-------------------|
| Bad code line | Localized problem — affects one function/file |
| Bad plan line | Hundreds of cascading errors — wrong strategy pollutes implementation |
| Bad research line | Thousands of downstream failures — architectural misunderstandings compound exponentially |

**Implication:** Invest most review effort in the research phase. Human review at the research/plan boundary has the highest leverage.

## Context Utilization Target

Target 40-60% of available context window. Beyond this threshold, model ability to accurately recall information degrades. The final 20% of context capacity is the performance degradation zone — avoid starting complex tasks when approaching this threshold.

## Subagent Isolation for Context Preservation

For codebases exceeding 100k LOC, use subagents to isolate context:

- Main conversation stays clean — subagents return only final answers
- Create a ~5,000 token markdown specification covering key components and architecture
- Feed the spec as context rather than allowing full repository exploration
- Focus each subagent on one directory or concern at a time

## Compaction Artifact Template

WHEN approaching context limits, structure persistent state as:

```markdown
## Compaction Artifact — [task name]

### Goal
[One-sentence current objective]

### Approach
[Chosen strategy and rationale — why this approach over alternatives]

### Completed Steps
- [Step 1: what was done and outcome]
- [Step 2: what was done and outcome]

### Active Blockers
- [Blocker description and what's needed to resolve]

### Next Immediate Steps
1. [Next action with specific details]
2. [Following action]
```

Store as markdown files in the working directory or encode in commit messages. After compaction, the agent reads this artifact to restore state.

## Multi-Claude Workflows

Patterns for parallel verification and concurrent work:

| Pattern | How | Use When |
|---------|-----|----------|
| **Write + Review** | One Claude writes code, another reviews | Code quality gates, security-sensitive changes |
| **Parallel features** | Separate git worktrees, one Claude per feature | Independent features that don't share files |
| **Fan-out analysis** | Multiple subagents each analyze one component | Large codebase understanding, audit tasks |

Use `git worktree` for lightweight branch isolation when running parallel Claude instances.

## Headless Mode Patterns

For automation, CI/CD, and scripted workflows:

- **`-p` flag** — Single prompt, non-interactive execution
- **`--output-format stream-json`** — Structured output for programmatic consumption
- **`--allowedTools`** — Restrict tool access for safety in automated contexts
- **Fan-out** — Launch parallel headless invocations for independent subtasks

Example: `claude -p "analyze src/auth/ for security issues" --output-format stream-json --allowedTools Read Grep Glob`
