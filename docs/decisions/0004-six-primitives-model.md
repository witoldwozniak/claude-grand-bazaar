---
title: "ADR-0004: Five Primitives Model"
description: "Plugin composition from exactly five primitives: Skills, Hooks, Subagents, Connectors, and LSP servers."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Five Primitives Model

## Context and Problem Statement

Claude Code plugins need a composition model — a defined set of building blocks that plugin authors combine to create functionality. Without a fixed vocabulary of primitives, plugins would be ad-hoc collections of files with no predictable structure, making them harder to build, document, and reason about.

The question: what building blocks should plugins compose from, and how many is the right number?

The original model defined six primitives (Skills, Hooks, Agents, MCP servers, LSP servers, Commands). Experience and Claude Code's own evolution prompted a revision: Commands were absorbed into Skills (a Skill can be both context-triggered and user-invoked), "Agents" was renamed to "Subagents" to clarify their role as focused specialists rather than top-level orchestrators, and "MCP servers" was renamed to "Connectors" to emphasize their purpose over their protocol.

## Considered Options

1. Five named primitives with distinct roles (Skills, Hooks, Subagents, Connectors, LSP servers)
2. Fewer primitives — collapse further (e.g., merge Hooks into Skills)
3. Open-ended primitive set — let plugin authors define their own building block types

## Decision Outcome

Chosen option: "Five named primitives with distinct roles", because each primitive addresses a genuinely different concern and collapsing any two would lose meaningful distinctions.

### Consequences

**Good:**

- Each primitive has a single, clear purpose: Skills inform, Hooks enforce, Subagents focus, Connectors connect, LSP servers perceive.
- Plugin authors have a concrete vocabulary for describing what their plugin does and how it works.
- The fixed set makes composition predictable — you know what kinds of things can appear in a plugin.
- Documentation and tooling can target specific primitive types.
- Absorbing Commands into Skills reduced the learning surface without losing functionality — user-invocable behavior is now a Skill attribute, not a separate primitive.

**Bad:**

- Five is a non-trivial number to learn for new plugin authors.
- Some primitives (LSP, Connectors) require deeper platform knowledge than others (Skills).
- The set is frozen — adding a sixth primitive later would be a significant change across the ecosystem.

## Pros and Cons of the Options

### Five Named Primitives

- Good, because each maps to a real, distinct capability in Claude Code's extension surface.
- Good, because the role distinctions prevent confusion (e.g., "should this be a hook or a skill?" has a clear answer based on enforcement vs. guidance).
- Good, because plugins can use any subset — a skill-only plugin is valid, as is one combining all five.
- Good, because the Commands → Skills collapse was validated by Claude Code's own changelog, which unified invocation and context-triggered behavior.
- Bad, because the taxonomy must be learned upfront.

### Fewer Primitives

- Good, because fewer concepts to learn.
- Bad, because collapsing Hooks into Skills loses the deterministic-vs-probabilistic distinction — Hooks enforce mechanically, Skills guide through prose.
- Bad, because treating LSP as a Connector variant loses the real-time perception model — LSP servers see code as it changes, Connectors respond to requests.
- Bad, because fewer categories means each category does more, making individual primitives harder to understand.

### Open-Ended Primitive Set

- Good, because maximum flexibility for plugin authors.
- Bad, because no shared vocabulary — every plugin invents its own structure.
- Bad, because tooling and documentation cannot anticipate what a plugin contains.
- Bad, because composition becomes unpredictable when plugins don't share a structural model.

## More Information

- [Doctrine: The Five Primitives](../development/DOCTRINE.md) — defines each primitive's role
- [Primitives documentation](../primitives/) — detailed guidelines per primitive
- [ADR-0003: Platform Compatibility Strategy](./0003-platform-compatibility-strategy.md) — Cowork supports three of the five primitives
