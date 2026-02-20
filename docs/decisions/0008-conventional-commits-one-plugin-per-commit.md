---
title: "ADR-0008: Conventional Commits with One Plugin Per Commit"
description: "Conventional Commits format with scoping strategy: plugin names for plugin work, topic scopes for repository-wide work."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Conventional Commits with One Plugin Per Commit

## Context and Problem Statement

The Grand Bazaar is a monorepo containing multiple independently versioned plugins alongside shared infrastructure (doctrine, PDLC, marketplace tooling). Commit history needs to serve two purposes: communicating the nature of changes to humans, and enabling per-plugin version tracking. Standard commit conventions don't account for multi-artifact repositories where each artifact versions independently and repository-wide work also needs clear attribution.

What commit format and scoping strategy should the project use?

## Considered Options

1. Conventional Commits with a scoping strategy — plugin names for plugin work, topic scopes for repository-wide work, one plugin per commit
2. Conventional Commits without scope constraints — allow cross-plugin commits
3. Free-form commit messages with plugin tags

## Decision Outcome

Chosen option: "Conventional Commits with a scoping strategy", because the format is well-established, the scope field naturally accommodates both plugin names and topic-based attribution, and independent plugin versioning requires cleanly filterable per-plugin history.

### Consequences

**Good:**

- Conventional Commits provides a well-known `type(scope): description` format with broad tooling support.
- Plugin-scoped commits (`feat(plugin-authoring): ...`) make each plugin's history cleanly extractable by filtering on scope.
- Topic-scoped commits (`docs(doctrine): ...`, `chore(marketplace): ...`, `fix(pdlc): ...`) give repository-wide work clear attribution without forcing it into a plugin's history.
- Commit types (`feat`, `fix`, etc.) map directly to version bump decisions.
- Breaking changes are explicitly flagged with `!` suffix and `BREAKING CHANGE:` footer.
- The one-plugin-per-commit rule keeps version histories clean — a commit touching three plugins would pollute all three histories.

**Bad:**

- Changes that ripple across many plugins require separate commits per plugin — more commits, more ceremony.
- Developers must remember to split work that touches multiple plugins into separate commits.
- The scoping strategy (plugin name vs. topic scope) must be learned alongside the format itself.

## Pros and Cons of the Options

### Conventional Commits + Scoping Strategy

- Good, because per-plugin history is clean — `git log --grep="(plugin-name)"` gives you exactly that plugin's changes.
- Good, because topic scopes (`doctrine`, `marketplace`, `pdlc`) prevent repository-wide work from being orphaned or mislabeled.
- Good, because the `type(scope): description` format naturally accommodates both use cases without special syntax.
- Bad, because the one-plugin rule adds friction for cross-cutting changes.

### Conventional Commits Without Constraint

- Good, because developers can commit naturally without splitting work.
- Bad, because a commit touching three plugins pollutes all three plugins' version histories.
- Bad, because it becomes unclear which plugin a `feat` applies to when the commit spans multiple.

### Free-Form with Tags

- Good, because no format to learn.
- Bad, because inconsistent messages make history harder to parse.
- Bad, because no standard tooling can extract version-relevant information.
- Bad, because plugin attribution requires manual inspection of each commit's diff.

## More Information

- [Git Conventions](../development/GIT.md) — full commit format, types, scopes, and branch naming
- [ADR-0005: No Inter-Plugin Dependencies](./0005-no-inter-plugin-dependencies.md) — the independence model that makes per-plugin history valuable
- [Versioning Strategy](../development/VERSIONING.md) — how commit types inform version bumps
