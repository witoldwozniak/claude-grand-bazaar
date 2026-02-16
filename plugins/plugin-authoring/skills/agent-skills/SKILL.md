---
name: agent-skills
description: Guide for creating, evaluating, and improving agent skills. Use when creating a new skill, updating an existing skill, writing SKILL.md files, organizing skill content, reviewing skill design, auditing skill quality, or assessing skill effectiveness. Triggers include "create a skill", "build a skill", "evaluate this skill", "review my skill", "audit this skill", "improve this skill", "how can I make this skill better". Not for reviewing application code or general code review.
author: witoldwozniak
license: Hippocratic-3.0
---

# Agent Skills

## Core Principles

### Concise is Key

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece: "Does this paragraph justify its token cost?" Prefer concise examples over verbose explanations.

### Degrees of Freedom

Match specificity to the task's fragility and variability:

| Freedom Level | When to Use | Form |
|---------------|-------------|------|
| **High** | Multiple approaches valid, context-dependent | Text-based instructions |
| **Medium** | Preferred pattern exists, some variation acceptable | Pseudocode or parameterized scripts |
| **Low** | Fragile operations, consistency critical | Specific scripts, few parameters |

Think of Claude exploring a path: a narrow bridge needs specific guardrails (low freedom), an open field allows many routes (high freedom).

### Token Budget Awareness

CLAUDE.md files load at session start and become part of every prompt — target 800-1,300 tokens lean, 5,000 max. SKILL.md content sizing follows the same principle: every paragraph must justify its token cost. Use tiered documentation — move depth to `references/` files, reducing baseline context. See [token-awareness.md](references/token-awareness.md) for sizing guidance and MCP server context costs.

### Progressive Disclosure

Skills use a three-level loading system:

1. **Metadata (name + description)** — Always in context (~100 words)
2. **SKILL.md body** — When skill triggers (<5k words)
3. **Bundled resources** — As needed (scripts can execute without loading into context)

For narrow skills (single concern), keep SKILL.md under ~500 lines. Meta-skills (gateway/router) can be longer when the additional length is routing infrastructure (decision trees, reference overviews, conditional loading guidance). The test for both: "Could this section move to a reference without hurting Claude's ability to route to the right resource?" If yes, move it.

See `references/progressive-disclosure.md` for disclosure patterns and detailed guidelines.

---

## Skill Structure

### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Configuration fields that control skill behavior. Only `name` and `description` are required. The `description` is the primary triggering mechanism — include both what the skill does and specific triggers/contexts for when to use it. All "when to use" information belongs here, not in the body.

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | ≤64 chars, kebab-case, must match folder name |
| `description` | Yes | ≤1024 chars, WHAT + WHEN, no XML tags |
| `author` | No | Author identifier |
| `license` | No | License identifier |
| `allowed-tools` | No | Tools the skill can use (array) |
| `metadata` | No | Arbitrary key-value metadata |
| `compatibility` | No | Compatibility constraints (≤500 chars) |
| `model` | No | Override model: `sonnet` / `opus` / `haiku` / `inherit` |
| `context` | No | Execution context: `fork` (isolated) or default (main conversation) |
| `agent` | No | Agent to execute the skill (requires `context: fork`) |
| `disable-model-invocation` | No | When `true`, skill cannot be auto-invoked by model |
| `user-invocable` | No | When `true`, skill appears as a `/command` for users |
| `hooks` | No | Lifecycle hooks scoped to this skill's execution |
- **Body** (Markdown): Instructions and guidance. Only loaded after the skill triggers.

#### Description Guidelines

- State WHAT (specific capability) and WHEN (trigger scenarios with "Use when...")
- Include keywords matching natural user phrasings
- Write in third person
- ≤1024 chars, no XML tags

Example: `"Document creation, editing, and analysis with tracked changes support. Use when working with .docx files for creating, modifying, or adding comments."`

#### Naming Rules

- `name`: ≤64 chars, lowercase alphanumeric + hyphens only, no `--`, doesn't start/end with `-`
- `name` must match the folder name

#### Variable Substitutions

Skills support variable substitution in the body:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | Full argument string passed when skill is invoked |
| `$ARGUMENTS[N]` | Nth argument (0-indexed) |
| `${CLAUDE_SESSION_ID}` | Current session identifier |

#### Dynamic Context Injection

Use `!command!` syntax in SKILL.md to inject dynamic content at load time:

```markdown
Current git branch: !git branch --show-current!
```

The command output replaces the `!command!` block when the skill loads. Use for environment-specific context that changes between sessions.

#### SKILL.json Alternative

Skills can use `SKILL.json` instead of `SKILL.md` for programmatic skill definitions. JSON format uses the same fields as frontmatter, with `instructions` replacing the markdown body. Prefer `SKILL.md` for human-authored skills; use `SKILL.json` for generated or tool-managed skills.

### Bundled Resources (optional)

#### Scripts (`scripts/`)

Executable code for tasks requiring deterministic reliability or repeatedly rewritten logic.

- **When to include**: Same code rewritten repeatedly, or deterministic reliability needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation
- Token efficient, deterministic, may execute without loading into context

#### References (`references/`)

Documentation loaded as needed to inform Claude's process.

- **When to include**: Documentation Claude should reference while working
- **Examples**: Database schemas, API docs, domain knowledge, company policies
- Keeps SKILL.md lean; loaded only when Claude determines it's needed
- For files >10k words, include grep search patterns in SKILL.md
- Information should live in either SKILL.md or references, not both

#### Assets (`assets/`)

Files used in output, not loaded into context.

- **When to include**: Templates, images, boilerplate used in final output
- **Examples**: `assets/logo.png`, `assets/slides.pptx`, `assets/frontend-template/`

### What NOT to Include

Do not create extraneous files: README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, etc. A skill contains only what an AI agent needs to do the job.

### Structure Patterns

SKILL.md can serve different architectural roles:

| Pattern | Role | SKILL.md Contains |
|---------|------|-------------------|
| **Narrow Skill** | Single concern | Instructions + workflow |
| **Meta-Skill / Gateway** | Router into subtopics | Routing table + decision guidance |

**Meta-Skill pattern**: SKILL.md acts as a routing table, not an instruction set. References contain the actual domain knowledge. SKILL.md must contain enough context for Claude to pick the right reference without reading them all — use decision trees or conditional guidance for ambiguous cases.

Good for: domains that decompose into distinct subtopics (git conventions, document processing, API patterns).
Risky for: domains where knowledge is deeply interconnected and most tasks need multiple references loaded.

---

## Workflows

| Intent | Reference | Summary |
|--------|-----------|---------|
| Creating or updating a skill | Read `references/creation-workflow.md` | 7-step process: gather examples, plan resources, init, edit, package, test (TDD), iterate |
| Evaluating, auditing, or reviewing a skill | Read `references/assessment-workflow.md` | Structured evaluation: spec checks, observations (5 areas), prioritized recommendations |

Route based on the user's request. When intent is ambiguous, ask to clarify whether they want to create/modify or evaluate.

**Context discipline:** Use `/compact` at 70% capacity during skill development sessions — don't wait for auto-compact at 95%. For long sessions, use the Document & Clear pattern: have Claude write progress to a markdown file, clear context, then continue from the file.

---

## Writing Style

### Body: Imperative/Infinitive Form

- "Extract text using pdfplumber" (imperative)
- "To rotate a PDF, use the rotate_pdf.py script" (infinitive)
- "Run the script with --angle parameter" (imperative)

Avoid second person ("You should extract...") and gerunds for instructions ("Extracting text is done...").

### Description: Third Person

- "Use when working with PDF files" — not "I use this when..." or "You should use this when..."

---

## Anti-patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Tutorial | Explains basics ("what is X") | Delete; link external docs if needed |
| Dump | SKILL.md contains content that could move to references without hurting routing | Move details to references/; narrow skills ~500 lines, meta-skills can be longer for routing infrastructure |
| Orphan | Reference files never loaded | Add explicit triggers in workflow |
| Vague Warning | "Be careful", "avoid errors" | Replace with specific prohibition + reason |
| Wrong Location | Trigger info only in body | Move to description field |
| Over-Engineered | README, CHANGELOG, etc. | Delete auxiliary files |
| Weak Trigger | `description: Helps with documents` | Add specific WHAT + WHEN + keywords |
| Inline Bloat | 8000 words of schemas in body | Core workflow in body, details in references/ |
| Second Person | "You should extract text..." | "Extract text..." |
