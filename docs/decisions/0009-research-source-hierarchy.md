---
title: "ADR-0009: Research Source Hierarchy"
description: "Three-tier hierarchy: academic and industry labs > direct experience with Claude Code > community practice; flexes by domain."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Research Source Hierarchy

## Context and Problem Statement

The Grand Bazaar's doctrine states "we study before we sell" — plugins must be research-grounded. But "research" can mean anything from peer-reviewed papers to blog posts to personal experience. Without a source hierarchy, the claim of being "research-grounded" has no teeth.

At the same time, some domains the Bazaar covers (like Claude Code hooks) have no academic literature at all. A rigid hierarchy that demands academic sources for every decision would block work in frontier areas.

How should we prioritize sources, and how should the hierarchy adapt to domains where the best sources vary?

## Considered Options

1. Three-tier hierarchy — (1) academic research and industry labs, (2) direct experience with Claude Code, (3) community practice — flexing by domain
2. Strict academic-first — require peer-reviewed sources for all foundational claims
3. Pragmatic — use whatever sources are available, no hierarchy

## Decision Outcome

Chosen option: "Three-tier hierarchy", because it provides a clear default preference while acknowledging that the best available source varies by domain.

### Consequences

**Good:**

- Clear default: prefer vetted, rigorous sources when they exist.
- Tier 2 (direct experience) explicitly validates hands-on work with Claude Code — we build plugins daily and discover things no paper covers. This is a legitimate source tier, not a fallback.
- Tier 3 (community practice) is permitted as primary evidence in frontier domains where academia is silent, treated with extra caution.
- The hierarchy is a guide for rigor, not a bureaucratic checklist — the principle is "best available source," not "only academic sources."

**Bad:**

- "Flexes by domain" requires judgment — two researchers might disagree on whether a domain qualifies as frontier.
- Community sources require extra scrutiny that isn't always well-defined.

## Pros and Cons of the Options

### Three-Tier Hierarchy

- Good, because it acknowledges reality — Claude Code-specific mechanics have no academic coverage, and waiting for papers would block all work.
- Good, because direct experience (tier 2) is recognized as a distinct, legitimate source — not lumped in with community practice or dismissed as anecdotal.
- Good, because the hierarchy still defaults to the most rigorous available source, preventing lazy reliance on blog posts when papers exist.
- Good, because it pairs with the research guidelines' emphasis on documenting method and citing sources.
- Bad, because the flex point is a judgment call that could be applied too liberally.

### Strict Academic-First

- Good, because it maximizes rigor for claims that underpin plugin opinions.
- Bad, because it would block work in most Claude Code-specific domains — hooks, agent orchestration, skill design have no academic literature.
- Bad, because some well-established disciplines (e.g., TDD) have both academic research and rich community practice — dismissing the community practice would miss valuable signal.

### Pragmatic (No Hierarchy)

- Good, because no rules to interpret or argue about.
- Bad, because "research-grounded" becomes meaningless — a plugin citing a single blog post meets the same bar as one citing peer-reviewed studies.
- Bad, because it provides no guidance for researchers on where to look or how much to trust what they find.

## More Information

- [Doctrine: Research-Based Development](../development/DOCTRINE.md) — the hierarchy statement and domain-flex principle
- [Research Guidelines](../research/_GUIDE.md) — file conventions, Definition of Done, and academic rigor guidance
