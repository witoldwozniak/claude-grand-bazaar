---
title: "ADR-0007: SemVer Hard/Soft Contract Split"
description: "Hard contracts (MCP/LSP/Hooks) get strict SemVer; soft contracts (Skills/Agents) use judgment."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# SemVer Hard/Soft Contract Split

## Context and Problem Statement

The Grand Bazaar uses Semantic Versioning, but not all primitives have the same kind of interface. MCP servers, LSP servers, and hooks have mechanically verifiable contracts — protocols, event triggers, schemas. Skills and agents have prose-based interfaces consumed by an LLM, where "breaking" is a judgment call because the model adapts gracefully.

How should SemVer apply across primitives with fundamentally different interface characteristics?

## Considered Options

1. Split approach — strict SemVer for hard contracts (MCP, LSP, Hooks), judgment-based SemVer for soft contracts (Skills, Agents)
2. Uniform strict SemVer — apply the same mechanical rules to all primitives
3. Uniform loose SemVer — treat all version bumps as advisory signals for humans

## Decision Outcome

Chosen option: "Split approach", because the nature of the interface determines whether breakage is mechanically detectable, and the versioning contract should reflect that reality.

### Consequences

**Good:**

- Hard-contract MAJOR bumps reliably signal "something you depend on changed mechanically" — users on auto-update know to pay attention.
- Soft-contract versioning communicates intent without false precision — a skill rewrite isn't the same kind of break as a removed MCP tool.
- The split acknowledges the LLM's role as an adapter layer for prose-based interfaces.

**Bad:**

- Two mental models for versioning within the same plugin system.
- Soft-contract MAJOR decisions require judgment, which means different authors might version similar changes differently.

## Pros and Cons of the Options

### Split Approach

- Good, because it matches reality — breaking an MCP schema is objectively different from rewriting a skill.
- Good, because hard-contract consumers (scripts, integrations) get reliable compatibility signals.
- Good, because soft-contract consumers (the LLM) don't trigger false MAJOR bumps over changes the model handles gracefully.
- Bad, because plugin authors must understand which versioning rules apply to which primitives.

### Uniform Strict SemVer

- Good, because one rule set is simpler to learn and apply.
- Bad, because "breaking change" has no clear mechanical definition for prose consumed by an LLM — every skill edit would need subjective classification.
- Bad, because it would produce frequent MAJOR bumps for skill refinements that don't actually break anything in practice.

### Uniform Loose SemVer

- Good, because no false precision for any primitive type.
- Bad, because hard-contract consumers lose reliable compatibility signals — a script depending on an MCP server's tool list can't trust MINOR bumps to be safe.
- Bad, because it undermines the trust that auto-updating users place in version numbers.

## More Information

- [Versioning Strategy: Hard/Soft Contract Split](../development/versioning.md) — full breakdown with per-primitive MAJOR/MINOR/PATCH tables
- [ADR-0004: Six Primitives Model](./0004-six-primitives-model.md) — the primitives being versioned
