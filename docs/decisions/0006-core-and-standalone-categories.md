---
title: "ADR-0006: Core and Standalone Plugin Categories"
description: "Two plugin categories: core (composable disciplines) and standalone (self-contained domains)."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Core and Standalone Plugin Categories

## Context and Problem Statement

The marketplace will contain plugins spanning very different domains — from software engineering disciplines (testing, documentation, project management) to niche interests (Minecraft modding, newsletter management). Some plugins benefit from careful composition with each other, while others are self-contained by nature.

Should all plugins be held to the same composition standard, or should the marketplace recognize different categories with different expectations?

## Considered Options

1. Two categories: core (composable disciplines) and standalone (self-contained domains)
2. Single category — all plugins held to the same composition standard
3. Multiple tiers — a gradient of composition expectations (core, extended, community, etc.)

## Decision Outcome

Chosen option: "Two categories: core and standalone", because the distinction between discipline-oriented plugins that must compose and domain-specific plugins that stand alone is real and worth encoding.

### Consequences

**Good:**

- Core plugins are designed as a coherent system — installing multiple core plugins produces a better experience than any individual plugin.
- Standalone plugins are free from composition overhead — a Minecraft modding plugin doesn't need to worry about composing with the testing plugin.
- The distinction sets clear expectations for both plugin authors and users.

**Bad:**

- The boundary between core and standalone may not always be obvious for new plugins.
- Core plugin authors bear additional design cost — they must verify composition with every other core plugin.

## Pros and Cons of the Options

### Two Categories

- Good, because it matches reality — some domains naturally compose (testing + documentation + PM) while others don't (newsletter management + Minecraft modding).
- Good, because it frees standalone plugins from unnecessary integration work.
- Good, because core plugins can be designed as a system, not just a collection.
- Bad, because categorization decisions may be contentious for borderline plugins.

### Single Category

- Good, because simpler mental model — all plugins are equal.
- Bad, because forcing composition requirements on self-contained domains wastes effort.
- Bad, because without the core designation, no plugins are designed to work together as a system — composition becomes accidental rather than intentional.

### Multiple Tiers

- Good, because finer-grained categorization might capture more nuance.
- Bad, because more categories means more rules to learn and more boundaries to police.
- Bad, because the current scale doesn't justify the complexity — two categories are sufficient.

## More Information

- [Doctrine: Composability](../doctrine.md) — defines core (main hall) and standalone (side alleys) distinction
- [ADR-0005: No Inter-Plugin Dependencies](./0005-no-inter-plugin-dependencies.md) — plugins compose through scoping, not through code dependencies
