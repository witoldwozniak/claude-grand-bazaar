---
title: "ADR-0003: Platform Compatibility Strategy"
description: "Claude Code as primary target with five primitives, Cowork as secondary target supporting three of the five."
status: accepted
date: 2026-02-15
decision-makers:
  - witoldwozniak
---

# Platform Compatibility Strategy

## Context and Problem Statement

Cowork (launched January 2026) shares Claude Code's plugin format — same `plugin.json` manifests, same directory structure, same `marketplace.json` catalogs. However, Cowork supports only three of the five primitives: Skills, Subagents, and Connectors. It does not support Hooks or LSP servers.

The Bazaar needs a stance: how do we handle this partial overlap? We build opinionated plugins from five primitives, but a meaningful subset of those plugins will work on Cowork with zero modification. Ignoring Cowork wastes reach; bending toward it risks weakening plugins.

## Considered Options

1. Claude Code-only — ignore Cowork entirely
2. Dual-target — build for both platforms, constraining plugins to the three shared primitives
3. Claude Code-first with Cowork compatibility tagging

## Decision Outcome

Chosen option: "Claude Code-first with Cowork compatibility tagging", because it preserves the full design surface while extending reach to Cowork where plugins fit naturally.

### Consequences

**Good:**

- Plugins are never weakened to fit Cowork's subset. Hooks and LSP remain first-class primitives.
- Plugins that naturally use only Skills, Subagents, and Connectors reach both audiences with no extra work.
- The PDLC's Design stage checks platform compatibility, making the status explicit rather than accidental.
- A single `marketplace.json` repository serves both platforms — no format translation needed.

**Bad:**

- Plugins with hooks or LSP are Claude Code-only, limiting their reach. This is an accepted tradeoff — enforcement and perception primitives are too valuable to sacrifice for compatibility.
- Cowork is still a research preview; its plugin capabilities may change. Compatibility tagging may need revisiting.

## Pros and Cons of the Options

### Claude Code-only

- Good, because it simplifies everything — one platform, no compatibility concerns.
- Bad, because it ignores a growing audience of knowledge workers on Cowork who could benefit from skill-based and agent-based plugins.
- Bad, because the shared format means Cowork compatibility is often free — ignoring it wastes reach for no gain.

### Dual-target

- Good, because every plugin works everywhere.
- Bad, because it forbids hooks and LSP servers — two of the five primitives. Hooks provide deterministic enforcement that prompt-based instructions cannot guarantee. LSP provides real-time code intelligence. Giving these up to chase compatibility contradicts the Bazaar's design philosophy.
- Bad, because it lets the least capable platform constrain the most capable one.

### Claude Code-first with Cowork compatibility tagging

- Good, because it's the natural outcome of the research findings — the formats are already compatible, the overlap is well-defined.
- Good, because it requires minimal process overhead — just a design-time question ("does this need hooks or LSP?") and a review-time check.
- Good, because it extends reach without compromising design.
- Bad, because Cowork users may encounter plugins they can't use. Clear labeling in README mitigates this.

## More Information

- Doctrine: "Target and Portability" section reflects this decision
- PDLC: Design (Stage 3) includes platform compatibility checks
- Primitives: `docs/primitives/HOOKS.md` and `docs/primitives/LSP.md` carry platform notes marking them as Claude Code-only
