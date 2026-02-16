# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Grand Bazaar is a curated plugin marketplace for Claude Code. It ships opinionated, research-grounded plugins built from six primitives: **Skills** (knowledge/reasoning), **Hooks** (automated guardrails), **Agents** (focused craftsmen), **MCP servers** (external connections), **LSP servers** (real-time code intelligence), and **Commands** (user-invoked entry points). The marketplace is at v0.1.0. The first plugin — `plugin-authoring` (v0.3.0) — is implemented and serves as the template for future plugins.

## Repository Structure

- `README.md` — Public-facing philosophy and quality standards
- `docs/` — Documentation (Markdown with YAML frontmatter)
  - `doctrine.md` — Operational principles (the project's constitution)
  - `primitives/` — Guidelines and knowledge for the six primitives (Skills, Hooks, Agents, MCP, LSP, Commands)
  - `development/` — Development process and planning
    - `git.md` — Git conventions: branching, Conventional Commits, and merge strategy
    - `versioning.md` — Semantic Versioning strategy for plugins and marketplace
    - `pdlc.md` — Plugin Development Life Cycle: 9 stages from Concept to Tend
    - `research.md` — Research guidelines, file conventions, and Definition of Done
  - `decisions/` — Architecture Decision Records (MADR format, sequential numbering)
    - `_GUIDE.md` — How and when to write Architecture Decision Records
  - `research/` — Structured research documents (one file per question, YAML frontmatter, indexed by `scripts/index-research.py`)
  - `notes-to-process/` — Unstructured notes pending conversion to proper research documents
    - `todo.md` — Development backlog and brainstormed plugin ideas
- `scripts/` — Development and research utilities
- `.claude-plugin/marketplace.json` — Plugin registry metadata; defines plugin names, sources, and descriptions
- `.claude-plugin/.github/` — PR and Issue templates
- `plugins/` — Plugin implementations, each in its own subdirectory matching the `source` field in `marketplace.json`
  - `plugin-authoring/` — Tools for building Claude Code extensions (agents, skills, scripts)

## Working Style

**Ask early, assume less.** Use the AskUserQuestion tool eagerly when facing ambiguity — about scope, approach, naming, structure, or anything that could go multiple ways. Getting guidance early is always cheaper than assuming wrong and forcing fixes later. When in doubt, ask.

**Code Actual** is the human decision-maker. Major decisions — scope, approach, shipping — require explicit human approval.

**TODO markers in markdown:** `<!-- TODO(human): description -->` and `<!-- TODO(claude): description -->`. HTML comments — greppable in source, invisible in rendered output.

## Build and Development

**Plugins:** Live under `./plugins/` with each plugin in its own subdirectory. Each plugin contains its own manifest (`plugin.json`), agents, skills, and supporting scripts.

**Dependencies:** Python 3.12+ (scripts use stdlib only). `gh` CLI for GitHub access (`gh auth login`). If `gh` CLI is not authenticated, warn Code Actual and await resolution.

**Tests:** `pip install -r requirements-ci.txt` for pytest, then:

```
pytest tests/ -v
```

**Validation (mirrors CI checks — run before pushing):**

```
python scripts/index-research.py && python scripts/index-decisions.py   # regenerate indices
python scripts/validate_manifests.py       # marketplace.json + plugin.json structure
python scripts/validate_frontmatter.py     # YAML frontmatter in docs, agents, skills
python scripts/validate_links.py           # internal markdown links resolve
```

**Index freshness:** CI rejects PRs where index files are stale. After adding or editing docs in `research/` or `decisions/`, run the index scripts and commit the updated `_INDEX.md` files.

**Platform docs:** `python scripts/fetch-claude-code-docs.py` fetches Claude Code documentation from `code.claude.com` for local reference. Use `--list` to see available pages, `--only` to fetch a subset. Output is gitignored.

## Key Architectural Concepts

**Two categories of plugins:**

- **Core plugins** (main hall) — Software engineering disciplines (authoring, docs, testing, PM, frontend, backend, DB). Designed to compose with each other.
- **Standalone plugins** (side alleys) — Domain-specific tools (e.g., Minecraft modding, newsletter management). Self-contained, no obligation to integrate with core.

**Plugin composition model:** Skills for reasoning, Hooks for enforcement, Agents for focus, MCP servers for connection, LSP servers for perception, Commands for invocation. A single plugin may combine multiple primitives.

**Agent roles are functional, not theatrical.** A role earns its existence by producing meaningfully different output than an unscoped agent would. Agent teams are orchestration (lead delegates to specialists), not simulation.

## Plugin Anatomy

Each plugin lives at `plugins/<name>/` and follows this structure:

```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json       # Manifest: name, version, description, author, license
├── README.md
├── commands/             # Slash commands (markdown, filename = command name)
│   └── <command-name>.md
├── agents/               # Agent definitions (markdown with YAML frontmatter)
│   └── <agent-name>.md
└── skills/               # Skill packages
    └── <skill-name>/
        ├── SKILL.md      # Skill definition (markdown with YAML frontmatter)
        ├── LICENSE.txt
        ├── references/   # Supporting knowledge documents
        └── scripts/      # Python utilities for the skill
```

**Agent frontmatter fields:** `name`, `description` (with `<example>` trigger blocks), `model` (sonnet/opus/haiku/inherit), `color`, `tools` (comma-separated), `skills` (references to skill names). Optional: `hooks`, `mcpServers`, `maxTurns`.

**Skill SKILL.md frontmatter:** `name`, `description` (including trigger phrases), `author`, `license`. Optional: `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context`, `agent`, `hooks`.

**Command files:** Markdown files in `commands/` where the filename becomes the slash command name. Supports `$ARGUMENTS` and positional `$1`, `$2` variables.

**plugin.json manifest:**

```json
{
  "name": "plugin-name",
  "version": "0.3.0",
  "description": "...",
  "author": { "name": "username" },
  "license": "Hippocratic-3.0"
}
```

**marketplace.json** (at `.claude-plugin/marketplace.json`) has top-level fields `name`, `owner`, `metadata` (with `version`, `description`, `pluginRoot`), and a `plugins` array where each entry has `name`, `source` (directory name under `plugins/`), and `description`.

## Git Conventions

**Branches:** `<type>/<scope>/<slug>` — scope is the plugin name; drop it for cross-cutting changes. See `docs/development/git.md` for full conventions.

```
feat/plugin-authoring/skill-templates
fix/auto-format/multiline-regex
chore/normalize-line-endings
```

**Commits:** `<type>(<scope>): <description>` — scope is the plugin name or repo-level topic; omit when truly cross-cutting. See `docs/development/git.md` for full conventions.

Types: `feat` · `fix` · `docs` · `chore` · `refactor` · `test` · `style` · `ci`

**Pull Requests:** One issue = one PR · Link issue · Summarize changes · CI must pass · Code Reviewer approves · Squash merge

## Terminology

Capitalize GitHub constructs: **Issue**, **Milestone**, **Sub-Issue**. Use "problem" or "concern" instead of lowercase "issue" to avoid ambiguity. "bug" = the defect itself; "Bug Report" = the Issue tracking it. "task" and "work item" are safe generic terms for untracked work.

## Code Standards

**Code:** TDD default (document opt-outs) · Clarity over cleverness · Explicit error handling · Comment "why" not "what"

**Tests:** Unit tests = Software Engineer · Integration/e2e = Test Engineer · No flaky tests · Test behavior, not implementation

**Security:** No secrets in code · Validate external input · Fail secure

## Standards for Shipping

Every plugin must be: research-grounded (traceable to vetted sources), well-documented (stranger-readable), composable (no conflicts with other plugins), opinionated (takes a clear position), and tested in real work.

## Target Platform

Primary target is Claude Code (all six primitives). Cowork is a secondary target — it shares the plugin format but supports only four of the six: Skills, Agents, MCP servers, and Commands (no Hooks, no LSP). Plugins without hook or LSP dependencies work on both platforms. Design decisions are never compromised for Cowork compatibility.
