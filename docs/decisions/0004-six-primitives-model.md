---
title: "ADR-0004: Six Primitives Model"
description: "Plugin composition from exactly six primitives: Skills, Hooks, Agents, MCP servers, LSP servers, and Commands."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Six Primitives Model

## Context and Problem Statement

Claude Code plugins need a composition model — a defined set of building blocks that plugin authors combine to create functionality. Without a fixed vocabulary of primitives, plugins would be ad-hoc collections of files with no predictable structure, making them harder to build, document, and reason about.

The question: what building blocks should plugins compose from, and how many is the right number?

## Considered Options

1. Six named primitives with distinct roles (Skills, Hooks, Agents, MCP servers, LSP servers, Commands)
2. Fewer primitives — collapse related concepts (e.g., merge Skills and Commands)
3. Open-ended primitive set — let plugin authors define their own building block types

## Decision Outcome

Chosen option: "Six named primitives with distinct roles", because each primitive addresses a genuinely different concern and collapsing any two would lose meaningful distinctions.

### Consequences

**Good:**

- Each primitive has a single, clear purpose: Skills inform, Hooks enforce, Agents focus, MCP servers connect, LSP servers perceive, Commands invoke.
- Plugin authors have a concrete vocabulary for describing what their plugin does and how it works.
- The fixed set makes composition predictable — you know what kinds of things can appear in a plugin.
- Documentation and tooling can target specific primitive types.

**Bad:**

- Six is a non-trivial number to learn for new plugin authors.
- Some primitives (LSP, MCP) require deeper platform knowledge than others (Skills, Commands).
- The set is frozen — adding a seventh primitive later would be a significant change across the ecosystem.

## Pros and Cons of the Options

### Six Named Primitives

- Good, because each maps to a real, distinct capability in Claude Code's extension surface.
- Good, because the role distinctions prevent confusion (e.g., "should this be a hook or a skill?" has a clear answer based on enforcement vs. guidance).
- Good, because plugins can use any subset — a skill-only plugin is valid, as is one combining all six.
- Bad, because the taxonomy must be learned upfront.

### Fewer Primitives

- Good, because fewer concepts to learn.
- Bad, because collapsing Skills and Commands loses the automatic-vs-invoked distinction — Skills activate on context, Commands activate on user request.
- Bad, because treating LSP as an MCP variant loses the real-time perception model — LSP servers see code as it changes, MCP servers respond to requests.
- Bad, because fewer categories means each category does more, making individual primitives harder to understand.

### Open-Ended Primitive Set

- Good, because maximum flexibility for plugin authors.
- Bad, because no shared vocabulary — every plugin invents its own structure.
- Bad, because tooling and documentation cannot anticipate what a plugin contains.
- Bad, because composition becomes unpredictable when plugins don't share a structural model.

## More Information

- [Doctrine: The Six Primitives](../doctrine.md) — defines each primitive's role
- [Primitives documentation](../primitives/) — detailed guidelines per primitive
- [ADR-0003: Platform Compatibility Strategy](./0003-platform-compatibility-strategy.md) — Cowork supports four of the six primitives
