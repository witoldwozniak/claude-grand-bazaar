---
title: "ADR-0014: Documentation Architecture"
description: "Plugin documentation follows single-source-of-truth: README ships with plugin, primitive metadata extracted from structured files, research and design notes live externally."
status: accepted
date: 2026-02-16
decision-makers:
  - witoldwozniak
---

# Documentation Architecture

## Context and Problem Statement

The PDLC's Document stage originally listed five artifacts that ship with a plugin: README, research notes, primitive documentation, design decisions, and a composition guide. During concept work on plugin-authoring, this raised duplication concerns. Research notes and design decisions already live in GitHub Issues. Primitive behavior is already defined in structured files (SKILL.md frontmatter, agent markdown frontmatter, hook configs). Duplicating this information into separate documentation files creates maintenance burden and divergence risk.

How should plugin documentation be structured to maintain a single source of truth while still serving strangers who need to understand and use the plugin?

## Considered Options

1. Single source of truth — README ships with plugin, everything else extracted or external
2. Full artifact set — all five documents ship inside the plugin directory
3. External everything — no documentation ships with the plugin, marketplace site is the only docs

## Decision Outcome

Chosen option: "Single source of truth", because each piece of documentation should have exactly one canonical location, and duplication is a maintenance liability.

### Consequences

**Good:**

- **Plugin ships README only.** Hand-written, covers what/why/install/usage/opinion. This is the one artifact where human craft matters and scripting can't substitute.
- **Primitives are self-documenting.** SKILL.md, agent .md frontmatter, hook configs — these structured files ARE the primitive documentation. No separate per-primitive READMEs needed.
- **Research and design notes live externally.** GitHub Issues are the canonical record. Distilled summaries may live in `docs/` or the marketplace site, but they don't ship inside the plugin directory.
- **Marketplace site assembled programmatically.** Pulls plugin README, extracts primitive metadata from frontmatter, links to research/design notes, builds a reference index. Per-plugin page with sub-pages per primitive, plus a cross-plugin reference index.
- **Diataxis framework.** Bazaar documentation follows the Diataxis model — tutorials, how-to guides, reference, and explanation — ensuring each document serves a clear purpose and audience.
- No duplication means no divergence. One place to update, one place to read.

**Bad:**

- Plugin directory alone doesn't contain the full story — you need the marketplace site or GitHub Issues for research/design context.
- Programmatic assembly requires tooling. The marketplace site build depends on extraction scripts that must be maintained.
- Primitive documentation quality is constrained by what frontmatter can express. Complex behaviors may need supplementary explanation in the README.

## Pros and Cons of the Options

### Single Source of Truth

- Good, because no duplication — each fact lives in one place.
- Good, because structured files (SKILL.md, agent frontmatter) are already required by the plugin format, so documentation is a byproduct of building.
- Good, because the marketplace site can present documentation richer than any static file set — cross-references, search, primitive indexes.
- Bad, because the plugin directory isn't self-contained for full documentation — it depends on external systems for the complete picture.

### Full Artifact Set

- Good, because the plugin directory is entirely self-contained — everything a stranger needs is right there.
- Bad, because research notes and design decisions are duplicated from Issues — two sources of truth that will diverge.
- Bad, because per-primitive READMEs duplicate information already in SKILL.md and agent frontmatter.
- Bad, because maintenance burden scales with the number of artifacts per plugin.

### External Everything

- Good, because all documentation lives in one system (the marketplace site).
- Bad, because the plugin directory has no human-readable documentation at all — not even a README.
- Bad, because it creates a hard dependency on the marketplace site being available and functional.
- Bad, because it violates the expectation that a directory you install should explain itself.

## More Information

- [PDLC: Document stage](../development/PDLC.md) — updated to reference this ADR
- [Plugin Anatomy](../../CLAUDE.md) — plugin directory structure showing README, SKILL.md, and agent frontmatter locations
- [Doctrine: Documentation](../development/DOCTRINE.md) — the stranger test principle that documentation must satisfy
