---
title: Git Conventions
description: "Branching, commit, and merge conventions for the Claude Grand Bazaar."
---

# Git Conventions

_Draft — February 16, 2026_

## Overview

The Grand Bazaar uses GitHub Flow for branching and Conventional Commits 1.0.0 for commit messages. These conventions keep source history clean, attributable, and filterable per plugin.

Commit types map directly to version bumps — see the [Versioning Strategy](VERSIONING.md) for how commits drive plugin releases.

## Branching: GitHub Flow

The Bazaar follows [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow). There is one long-lived branch: `main`. All work happens on short-lived feature branches that merge back into `main` via pull request.

`main` is always the current state of the project. There are no `develop`, `release`, or `hotfix` branches. Plugins version independently — there is no monolithic release that would need stabilization on a separate branch.

### Branch Naming

Feature branches use the format `<type>/<scope>/<slug>`:

```
feat/prove-or-flag/hypothesis-first-workflow
fix/auto-format/multiline-regex
docs/doctrine/add-lsp-primitive
chore/ci/add-lint-step
```

The type and scope mirror the Conventional Commits vocabulary. The slug is a short description in lowercase with hyphens. For cross-cutting changes without a plugin scope, drop it:

```
chore/normalize-line-endings
docs/update-contributing-guide
```

### Merge Strategy

Squash merge when a feature branch contains messy interim commits and the logical change is one unit. Regular merge when the branch contains a clean sequence of commits that each tell part of the story. In either case, the resulting commit(s) on `main` must follow Conventional Commits format.

Delete branches after merge. Stale branches are noise.

## Commits: Conventional Commits

The Bazaar follows [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) for all commit messages.

### Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type       | Use                                                                             |
| ---------- | ------------------------------------------------------------------------------- |
| `feat`     | New capability — a new skill section, hook matcher, agent tool, server endpoint |
| `fix`      | Bug fix — regex correction, false positive, broken example                      |
| `docs`     | Documentation only — README, doctrine, guides, comments                         |
| `chore`    | Maintenance — dependency updates, CI config, gitignore                          |
| `refactor` | Restructuring without behavior change                                           |
| `test`     | Adding or updating tests                                                        |
| `style`    | Formatting, whitespace, punctuation — no logic change                           |
| `ci`       | CI/CD pipeline changes                                                          |

### Scopes

The primary scope is the plugin name, flat and unqualified:

```
feat(prove-or-flag): add coverage threshold guidance
fix(auto-format): correct regex for multiline blocks
docs(security-audit): rewrite getting started section
```

Plugin names are unique across the marketplace. No primitive type prefix — `fix(auto-format)` not `fix(hook/auto-format)`.

For repository-wide concerns — doctrine, marketplace infrastructure, lifecycle docs, CI — use the filename or topic as scope:

```
docs(doctrine): add LSP servers as fifth primitive
chore(marketplace): update catalog schema
docs(pdlc): add Tend stage
```

Repository-level scopes are not a fixed list. The repository structure is still evolving, and consistency within the current structure matters more than a premature taxonomy.

Commits that are truly cross-cutting don't need a scope:

```
chore: update gitignore
style: normalize line endings across repo
```

Don't force a scope where it adds no information.

### One Plugin Per Commit

A commit should touch at most one plugin. If a change affects two or more plugins, each plugin gets its own commit. This is non-negotiable for independent versioning — it ensures each plugin's history is cleanly filterable by scope.

For convention changes that ripple across many plugins (metadata format changes, naming updates), make separate commits per plugin. More commits is fine. Clean attribution is the priority.

### Breaking Changes

Use `!` after the type/scope to flag breaking changes:

```
feat(security-hook)!: change default event from PreToolUse to PostToolUse
feat(prove-or-flag)!: restructure around hypothesis-first workflow
```

Every commit with `!` must include a `BREAKING CHANGE:` footer explaining what changed and why:

```
feat(security-hook)!: change default event from PreToolUse to PostToolUse

Validation after tool execution catches a broader class of issues
than pre-execution filtering. Existing configurations that rely on
PreToolUse will need to update their hook event.

BREAKING CHANGE: Default hook event changed from PreToolUse to
PostToolUse. Update your .claude/hooks.json if you override the
default event.
```
