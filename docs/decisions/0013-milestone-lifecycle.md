---
title: "ADR-0013: Milestone Lifecycle & Maintenance"
description: "Plugin milestones close at Ship. Maintenance issues are free-standing, not tracked by a persistent Tend issue."
status: accepted
date: 2026-02-16
decision-makers:
  - witoldwozniak
---

# Milestone Lifecycle & Maintenance

## Context and Problem Statement

The PDLC defines nine stages from Concept to Tend. Each stage maps to a GitHub Issue within a plugin's Milestone. The Tend stage is ongoing — it has no exit. This raises a question: what happens to the milestone when the plugin ships?

The original PDLC draft kept the Tend issue open indefinitely and left the milestone open with it. This conflates two different things: the bounded work of building and shipping a plugin (Concept through Ship) and the unbounded work of maintaining it afterward.

## Considered Options

1. Milestone closes at Ship — maintenance issues are free-standing
2. Milestone stays open — Tend issue keeps it alive indefinitely
3. Separate maintenance milestone — new milestone created at Ship for ongoing work

## Decision Outcome

Chosen option: "Milestone closes at Ship", because milestones represent bounded work with a clear beginning and end.

### Consequences

**Good:**

- Milestones have a clean lifecycle: open at intake, close at Ship. Progress tracking is meaningful.
- Maintenance issues are free-standing, labeled `stage/maintenance` + `plugin/<name>`. They can be triaged, prioritized, and closed independently.
- Enhancements significant enough to rethink the plugin's opinion or scope spawn new milestones, re-entering the PDLC at Research or Design. This keeps the bounded/unbounded distinction clean.
- Small bug fixes and tweaks stay in Build scope as free-standing issues — no ceremony overhead.

**Bad:**

- Maintenance issues lack the visual grouping that a milestone provides. Filtering by label is the substitute.
- The threshold between "free-standing fix" and "new milestone" requires judgment. There's no formula — Code Actual decides.

## Pros and Cons of the Options

### Milestone Closes at Ship

- Good, because milestones represent bounded work — "build and ship this plugin" has a clear end.
- Good, because GitHub's milestone progress bar actually reaches 100% and the milestone closes.
- Good, because it forces explicit decisions about whether maintenance work is a tweak or a rethink.
- Bad, because maintenance work isn't grouped under a milestone — label-based filtering is less visual.

### Milestone Stays Open

- Good, because all work related to a plugin lives under one milestone forever.
- Bad, because the milestone never closes — progress tracking is permanently incomplete.
- Bad, because it conflates "building the plugin" with "maintaining it indefinitely."
- Bad, because a milestone with 8 closed issues and 1 perpetually open issue is misleading.

### Separate Maintenance Milestone

- Good, because it preserves milestone grouping for maintenance work.
- Bad, because a milestone with no end date and no fixed scope isn't really a milestone — it's a backlog.
- Bad, because it creates process overhead: every plugin now has two milestones, one closed and one permanently open.

## More Information

- [PDLC: Tend stage](../development/pdlc.md) — the ongoing maintenance stage
- [plugin-authoring Concept Capture: Tend](../notes-to-process/plugin-authoring-concept.md) — where this question was first identified
- Label convention: `stage/maintenance` for the PDLC stage, `plugin/<name>` for the plugin. "Tend" remains the PDLC stage name in prose; "maintenance" is the label name for practical searchability.
