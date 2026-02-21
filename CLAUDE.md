# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Claude Grand Bazaar is a curated plugin marketplace for Claude Code and Claude Cowork. It ships opinionated, research-grounded plugins built from five primitives: **Skills** (knowledge/reasoning), **Hooks** (automated guardrails), **Subagents** (focused specialists), **Connectors** (external connections), and **LSP servers** (real-time code intelligence). The marketplace is at v0.1.0. No plugins have shipped yet — `plugins/` is ready for the first plugin.

<!-- NOTE: As this file grows, extract domain-specific guidance into Skills. CLAUDE.md should stay a compact bootstrap — enough for Claude to orient, with Skills carrying the depth. -->

## Working Style

**Ask early, assume less.** Use the AskUserQuestion tool eagerly when facing ambiguity — about scope, approach, naming, structure, or anything that could go multiple ways. Getting guidance early is always cheaper than assuming wrong and forcing fixes later. When in doubt, ask.

**Code Actual** is the human decision-maker. Major decisions — scope, approach, shipping — require explicit human approval.

**Think critically.** Do not follow user requests blindly. If a request seems likely to introduce bugs, break conventions, or move in a questionable direction — say so. Propose alternatives. The goal is the best outcome, not unquestioning compliance.

**Prevent overengineering.** Solve the problem at hand, not hypothetical future problems. Avoid abstractions, configuration layers, or flexibility that nobody asked for. When in doubt, write the simpler version.

**TODO markers in markdown:** `<!-- TODO(github-username): description -->` and `<!-- TODO(claude): description -->`. HTML comments — greppable in source, invisible in rendered output.

## Build and Development

**Plugins:** Live under `./plugins/` with each plugin in its own subdirectory. Each plugin contains its own manifest (`plugin.json`), agents, skills, and supporting scripts.

**Dependencies:** Python 3.12+ (scripts use stdlib only). `gh` CLI for GitHub access (`gh auth login`). If `gh` CLI is not authenticated, warn Code Actual and await resolution.

**Tests:** `pip install -r requirements-ci.txt` for pytest, then:

```
pytest tests/ -v
```

**Validation (mirrors CI checks — run before pushing):**

```
python scripts/index_research.py && python scripts/index_decisions.py   # regenerate indices
python scripts/validate_manifests.py       # marketplace.json + plugin.json structure
python scripts/validate_frontmatter.py     # YAML frontmatter in docs, agents, skills
python scripts/validate_links.py           # internal markdown links resolve
```

**Index freshness:** CI rejects PRs where index files are stale. After adding or editing docs in `research/` or `decisions/`, run the index scripts and commit the updated `_INDEX.md` files.

**Platform docs:** `python scripts/fetch_claude_code_docs.py` fetches Claude Code documentation from `code.claude.com` for local reference. Use `--list` to see available pages, `--only` to fetch a subset. Output is gitignored. Fetched docs are at `docs/claude-code-docs`.

**Agent frontmatter fields:** `name`, `description` (with `<example>` trigger blocks), `model` (sonnet/opus/haiku/inherit), `color`, `tools` (comma-separated). Optional: `skills` (references to skill names), `hooks`, `mcpServers`, `maxTurns`.

**Skill SKILL.md frontmatter:** `name`, `description` (including trigger phrases), `author`, `license`. Optional: `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context`, `agent`, `hooks`.

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

**Markdown filenames:** UPPERCASE (`DOCTRINE.md`). Multi-word names use UPPER_SNAKE_CASE (`MY_GUIDE.md`). Index/guide files use `_PREFIX.md` format (`_GUIDE.md`, `_INDEX.md`).

## Architecture

```
claude-grand-bazaar/
  .claude-plugin/       # marketplace.json (marketplace manifest)
  docs/
    decisions/          # ADRs (NNNN-title.md) + _INDEX.md
    development/        # DOCTRINE.md, GIT.md, PDLC.md, VERSIONING.md
    primitives/         # One doc per primitive + _GUIDE.md
    research/           # Research docs + _INDEX.md
    claude-code-docs/   # Fetched platform docs (gitignored)
  plugins/              # One subdirectory per plugin (none shipped yet)
  scripts/              # Validation, indexing, and fetch scripts
  tests/                # pytest tests mirroring scripts/
```

## Gotchas

- **Index staleness:** CI will reject PRs if `_INDEX.md` files don't match. Always run `index_research.py` and `index_decisions.py` after touching `docs/research/` or `docs/decisions/`.
- **Validation mirrors CI:** Run all four validation commands before pushing — CI runs the same checks and failures block merge.
- **Plugin path in marketplace.json:** The `source` field in each plugin entry must match the actual directory name under `plugins/`. If a plugin is renamed or moved, update both.
- **Frontmatter is strict:** Agent and skill `.md` files require exact frontmatter fields. `validate_frontmatter.py` enforces required keys and allowed values (e.g., model must be sonnet/opus/haiku/inherit).
- **No runtime dependencies:** All Python scripts use stdlib only — never add third-party imports to `scripts/`.

## Git Conventions

See [docs/development/GIT.md](docs/development/GIT.md) for full conventions: branching (`<type>/<scope>/<slug>`), Conventional Commits (`<type>(<scope>): <description>`), and merge strategy.

## Terminology

Capitalize GitHub constructs: **Issue**, **Milestone**, **Sub-Issue**. Use "problem" or "concern" instead of lowercase "issue" to avoid ambiguity. "bug" = the defect itself; "Bug Report" = the Issue tracking it. "task" and "work item" are safe generic terms for untracked work.

Also capitalize Claude Code concepts: Skills, Agent Skills, Subagents, Hooks, Connectors (MCP Servers), LSP Servers, Commands, Slash Commands

## Code Standards

**Code:** Clarity over cleverness · Explicit error handling · Comment "why" not "what"

**Tests:** No flaky tests · Test behavior, not implementation

**Security:** No secrets in code · Validate external input · Fail secure

## Standards for Shipping

Every plugin must be: research-grounded (traceable to vetted sources), well-documented (stranger-readable), composable (no conflicts with other plugins), opinionated (takes a clear position), and tested in real work. See [Doctrine](docs/development/DOCTRINE.md).

## Target Platform

Primary target is Claude Code (all five primitives). Cowork is a secondary target — it shares the plugin format but supports three of the five: Skills, Subagents, and Connectors. Plugins without Hook or LSP dependencies work on both platforms. Design decisions are never compromised for Cowork compatibility. See [Doctrine](docs/development/DOCTRINE.md).
