---
title: "ADR-0008: Conventional Commits with One Plugin Per Commit"
description: "Conventional Commits format with scope=plugin-name; one plugin per commit for independent versioning."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Conventional Commits with One Plugin Per Commit

## Context and Problem Statement

The Grand Bazaar is a monorepo containing multiple independently versioned plugins. Commit history needs to serve two purposes: communicating the nature of changes to humans, and enabling per-plugin version tracking. Standard commit conventions don't account for multi-artifact repositories where each artifact versions independently.

What commit format should the project use, and how should commits relate to plugins?

## Considered Options

1. Conventional Commits with scope=plugin-name and a strict one-plugin-per-commit rule
2. Conventional Commits without the one-plugin constraint — allow cross-plugin commits
3. Free-form commit messages with plugin tags

## Decision Outcome

Chosen option: "Conventional Commits with scope=plugin-name and one-plugin-per-commit", because independent plugin versioning requires cleanly filterable per-plugin history.

### Consequences

**Good:**

- Each plugin's commit history is cleanly extractable by filtering on scope.
- Commit types (`feat`, `fix`, etc.) map directly to version bump decisions.
- Breaking changes are explicitly flagged with `!` suffix and `BREAKING CHANGE:` footer.
- Repository-wide changes use topic-based scopes (`doctrine`, `marketplace`, `pdlc`) keeping the format consistent.

**Bad:**

- Convention changes that ripple across many plugins require separate commits per plugin — more commits, more ceremony.
- Developers must remember to split work that touches multiple plugins into separate commits.

## Pros and Cons of the Options

### Conventional Commits + One Plugin Per Commit

- Good, because per-plugin history is clean — `git log --grep="(plugin-name)"` gives you exactly that plugin's changes.
- Good, because Conventional Commits is a well-known standard with tooling support.
- Good, because the `type(scope): description` format naturally accommodates plugin names as scopes.
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

- [Git Conventions](../development/git.md) — full commit format, types, scopes, and branch naming
- [ADR-0005: No Inter-Plugin Dependencies](./0005-no-inter-plugin-dependencies.md) — the independence model that makes per-plugin history valuable
- [Versioning Strategy](../development/versioning.md) — how commit types inform version bumps
