---
title: "ADR-0012: Contributions Post-v1"
description: "Direct contributions welcomed only after marketplace reaches v1.0."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Contributions Post-v1

## Context and Problem Statement

The Grand Bazaar is open source and aspires to community participation. However, the project is pre-v1.0 — foundational decisions are still crystallizing, the plugin format is evolving, and the quality bar is being established through the first batch of plugins. Accepting direct contributions (plugin submissions, PRs to core) before these foundations stabilize risks introducing inconsistency and creating obligations to support code that may not survive architectural shifts.

When should the Bazaar begin accepting direct contributions?

## Considered Options

1. Accept contributions after v1.0 — allow feedback channels now, direct contributions later
2. Accept contributions immediately — open to PRs and plugin submissions from day one
3. Never accept direct contributions — remain a single-maintainer project

## Decision Outcome

Chosen option: "Accept contributions after v1.0", because the project needs stable foundations before it can meaningfully review and integrate external work.

### Consequences

**Good:**

- The project can evolve its foundations without breaking contributor expectations.
- Quality standards are established through first-party plugins before being applied to external contributions.
- Feedback is welcomed immediately — Discussions, bug reports, change requests, and plugin requests are all open. The community can shape the project without the overhead of code review.

**Bad:**

- Enthusiastic early contributors must wait. Some may lose interest before v1.0.
- The project carries all development load internally until v1.0.

## Pros and Cons of the Options

### Contributions Post-v1

- Good, because the quality bar, plugin format, and architectural patterns stabilize before external code enters the codebase.
- Good, because it avoids the "early contributor code doesn't match evolved standards" problem.
- Good, because feedback channels (Discussions, bug reports, change requests, plugin requests) provide meaningful community input without the overhead of code contributions.
- Bad, because it limits the project's growth rate during the pre-v1.0 period.

### Accept Immediately

- Good, because more contributors means faster development and broader domain coverage.
- Bad, because contributors would build against unstable foundations — their work may need significant rework as the project evolves.
- Bad, because reviewing external contributions against an evolving quality bar creates friction and potential conflict.
- Bad, because maintaining backward compatibility with contributor code constrains architectural evolution.

### Never Accept

- Good, because full control over quality and direction is maintained permanently.
- Bad, because it caps the project's growth at what a single maintainer can produce.
- Bad, because it contradicts the doctrine's community orientation — "The Grand Bazaar is open and craves the hum of a crowd."
- Bad, because niche domains (Minecraft modding, newsletter management) are best served by people who work in those domains.

## More Information

- [Doctrine: Community](../doctrine.md) — community philosophy and the v1.0 contribution gate
