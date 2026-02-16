---
title: "ADR-0005: No Inter-Plugin Dependencies"
description: "Every plugin works in isolation; duplication preferred over coupling."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# No Inter-Plugin Dependencies

## Context and Problem Statement

As the marketplace grows, plugins will share common patterns — similar research methodologies, overlapping domain knowledge, shared utility scripts. The natural software engineering instinct is to extract shared code into a common dependency. But in a marketplace where users choose their own subset of plugins, shared dependencies create coupling between independently versioned artifacts.

Should plugins be allowed to depend on other plugins?

## Considered Options

1. No inter-plugin dependencies — every plugin works in isolation, duplication preferred over coupling
2. Allow declared dependencies — plugins can require other plugins, with version constraints
3. Shared libraries — extract common code into non-plugin packages that plugins can depend on

## Decision Outcome

Chosen option: "No inter-plugin dependencies", because users choose their own plugin subset and coupling between plugins would constrain that freedom.

### Consequences

**Good:**

- Users can install any combination of plugins without dependency resolution.
- Each plugin can be versioned, updated, and retired independently.
- No cascading breakage — a change to one plugin never breaks another.
- Plugin authors don't need to coordinate releases.

**Bad:**

- Code duplication when multiple plugins need similar functionality.
- Potential drift when duplicated patterns evolve differently across plugins.
- Plugin authors must be self-sufficient — they can't lean on other plugins for capabilities.

## Pros and Cons of the Options

### No Dependencies (Isolation)

- Good, because the marketplace model is "pick what you want" — dependencies would force unwanted installs.
- Good, because independent versioning is clean when there are no cross-plugin contracts.
- Good, because the blast radius of any change is confined to one plugin.
- Bad, because duplication is real and maintenance cost is higher per duplicated pattern.

### Declared Dependencies

- Good, because shared code lives in one place and stays consistent.
- Bad, because dependency resolution in a plugin marketplace adds significant complexity.
- Bad, because version conflicts between plugins become possible (plugin A needs v2 of shared, plugin B needs v1).
- Bad, because users lose the freedom to install exactly the plugins they want — dependencies pull in extras.

### Shared Libraries

- Good, because it centralizes common code without plugins depending on each other.
- Bad, because it creates a new artifact type that needs its own versioning and distribution.
- Bad, because it still introduces coupling — a library update can break multiple plugins.
- Bad, because the current scale (few plugins) doesn't justify the infrastructure.

## More Information

- [Versioning Strategy: Dependencies](../development/versioning.md) — "No inter-plugin dependencies" section
- [Doctrine: Composability](../doctrine.md) — "Everything is made to work well together, but nothing is mandatory"
