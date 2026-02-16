---
title: "ADR-0002: Plugin Customization Strategy"
description: "CLAUDE.md as the override layer for plugin customization — no new infrastructure needed."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Plugin Customization Strategy

## Context and Problem Statement

Plugins ship opinionated defaults — code review conventions, documentation rules, testing strategies. Some of these defaults will conflict with specific projects. The question is whether the Bazaar needs a customization mechanism so users can adapt plugin behavior to their context, or whether existing Claude Code infrastructure already covers this.

The tension is between the project's opinionated design principle (ship deliberate choices, not configuration surfaces) and the practical reality that conventions like commit formats, naming rules, and test coverage thresholds vary by project.

## Considered Options

1. Plugin-level configuration files (`.bazaar/<plugin>.yml`)
2. CLAUDE.md as the override layer (no new infrastructure)
3. A customization utility plugin that modifies other plugins

## Decision Outcome

Chosen option: "CLAUDE.md as the override layer", because it already exists, users already understand it, and it covers the prompt layer (skills, agents) without any new infrastructure. Hook scripts that need configurability can handle their own config as normal software design decisions, not as a Bazaar-wide system.

### Consequences

**Good:**

- Zero infrastructure to build or maintain.
- Users override plugin behavior using a mechanism they already know.
- Keeps the opinionated stance intact — defaults are the opinion, CLAUDE.md is the escape hatch.
- No config schema complexity to manage per plugin.

**Bad:**

- Hooks with hard-coded thresholds can't be overridden through CLAUDE.md since they execute outside Claude's reasoning. Users who disagree with a hook's threshold must fork the hook script.
- No standardized way to discover what a plugin's overridable behaviors are. Users need to read the skill/agent markdown to know what to contradict in CLAUDE.md.

## Pros and Cons of the Options

### Plugin-level configuration files

- Good, because it's a familiar pattern from developer tooling (ESLint, Prettier, Vale).
- Good, because it would give hooks a clean override path.
- Bad, because it's a customization layer on top of a customization layer — recursive complexity.
- Bad, because it requires designing, documenting, and validating a config schema per plugin.
- Bad, because it solves a problem nobody has reported yet.

### CLAUDE.md as the override layer

- Good, because it requires building nothing.
- Good, because Claude Code already reconciles conflicting instructions between skills and CLAUDE.md.
- Good, because it respects the existing mental model users have.
- Bad, because it doesn't cover hooks mechanically — only the prompt layer.
- Bad, because override discoverability depends on users reading plugin source.

### A customization utility plugin

- Good, because it centralizes override logic in one place.
- Bad, because it creates a meta-layer with dependency ordering problems.
- Bad, because it's premature abstraction — no evidence users want this.
- Bad, because it directly conflicts with the opinionated design principle.

## More Information

This decision emerged from a conversation on February 13, 2026 examining the tension between opinionated defaults and project-specific needs. The key insight was that the prompt layer (skills, agents) and the execution layer (hooks) have fundamentally different override mechanics, and only the prompt layer needs a general solution — which CLAUDE.md already provides.

Related: project doctrine on opinionated design (ship deliberate choices, not configuration surfaces).
