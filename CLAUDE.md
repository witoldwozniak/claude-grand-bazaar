# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Grand Bazaar is a curated plugin marketplace for Claude Code. It ships opinionated, research-grounded plugins built from five primitives: **Skills** (knowledge/reasoning), **Hooks** (automated guardrails), **Subagents** (focused specialists), **Connectors** (external connections), and **LSP servers** (real-time code intelligence). The marketplace is at v0.1.0. The first plugin — `plugin-authoring` (v0.3.0) — is implemented and serves as the template for future plugins.

<!-- NOTE: As this file grows, extract domain-specific guidance into Skills (plugin-authoring or new plugins). CLAUDE.md should stay a compact bootstrap — enough for Claude to orient, with Skills carrying the depth. -->

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
python scripts/index-research.py && python scripts/index-decisions.py   # regenerate indices
python scripts/validate_manifests.py       # marketplace.json + plugin.json structure
python scripts/validate_frontmatter.py     # YAML frontmatter in docs, agents, skills
python scripts/validate_links.py           # internal markdown links resolve
```

**Index freshness:** CI rejects PRs where index files are stale. After adding or editing docs in `research/` or `decisions/`, run the index scripts and commit the updated `_INDEX.md` files.

**Platform docs:** `python scripts/fetch-claude-code-docs.py` fetches Claude Code documentation from `code.claude.com` for local reference. Use `--list` to see available pages, `--only` to fetch a subset. Output is gitignored. Fetched docs are at `docs/claude-code-docs`.

**Agent frontmatter fields:** `name`, `description` (with `<example>` trigger blocks), `model` (sonnet/opus/haiku/inherit), `color`, `tools` (comma-separated), `skills` (references to skill names). Optional: `hooks`, `mcpServers`, `maxTurns`.

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

## Git Conventions

See [docs/development/GIT.md](docs/development/GIT.md) for full conventions: branching (`<type>/<scope>/<slug>`), Conventional Commits (`<type>(<scope>): <description>`), and squash-merge PRs.

## Terminology

Capitalize GitHub constructs: **Issue**, **Milestone**, **Sub-Issue**. Use "problem" or "concern" instead of lowercase "issue" to avoid ambiguity. "bug" = the defect itself; "Bug Report" = the Issue tracking it. "task" and "work item" are safe generic terms for untracked work.

Also capitalize Claude Code concepts: Skills, Agent Skills, Subagents, Hooks, Connectors (MCP Servers), LSP Servers, Commands, Slash Commands

## Code Standards

**Code:** Clarity over cleverness · Explicit error handling · Comment "why" not "what"

**Tests:** No flaky tests · Test behavior, not implementation

**Security:** No secrets in code · Validate external input · Fail secure

## Standards for Shipping

Every plugin must be: research-grounded (traceable to vetted sources), well-documented (stranger-readable), composable (no conflicts with other plugins), opinionated (takes a clear position), and tested in real work. See [Doctrine](docs/development/doctrine.md).

## Target Platform

Primary target is Claude Code (all five primitives). Cowork is a secondary target — it shares the plugin format but supports three of the five: Skills, Subagents, and Connectors. Plugins without Hook or LSP dependencies work on both platforms. Design decisions are never compromised for Cowork compatibility. See [Doctrine](docs/development/doctrine.md).
