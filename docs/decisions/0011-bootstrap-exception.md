---
title: "ADR-0011: Bootstrap Exception"
description: "plugin-authoring skips formal intake and bundles research capability temporarily."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Bootstrap Exception

## Context and Problem Statement

plugin-authoring encodes the PDLC as executable tooling — it is the plugin that enables building all other plugins. But it must exist before the process it encodes can run. This creates a bootstrapping problem: the standard PDLC requires formal intake (a Plugin Request that goes through triage) and assumes research tooling exists as a separate plugin. Neither condition holds for the first plugin.

Should plugin-authoring follow the standard process despite the circular dependency, or should it be granted explicit exceptions?

## Considered Options

1. Bootstrap exception — skip formal intake, bundle research capability temporarily
2. Full PDLC compliance — create the Plugin Request, follow standard intake, build research tooling first
3. Exempt the first plugin entirely — no process constraints for plugin-authoring

## Decision Outcome

Chosen option: "Bootstrap exception", because the deviations are scoped, documented, and temporary — they acknowledge the chicken-and-egg problem without abandoning the process entirely.

### Consequences

**Good:**

- plugin-authoring can be built without waiting for tooling that doesn't exist yet.
- The exception is explicitly scoped: implicit intake (self-evidently necessary) and bundled research capability (to be extracted later).
- Future plugins go through the standard process — the exception doesn't set a general precedent.
- When a dedicated `domain-research` plugin is extracted later, plugin-authoring drops its bundled research tooling. No inter-plugin dependency is created.

**Bad:**

- The first plugin doesn't fully validate the intake process it will enforce for others.
- Bundled research capability in plugin-authoring is a temporary duplication that must be actively cleaned up later.

## Pros and Cons of the Options

### Bootstrap Exception

- Good, because it's honest about the circular dependency — pretending to follow a process that requires tooling you're building is theater.
- Good, because the two deviations are narrow and documented.
- Good, because it explicitly states that future plugins don't get the same pass.
- Bad, because intake triage remains unvalidated until the second plugin goes through it.

### Full PDLC Compliance

- Good, because the first plugin would validate the entire process end-to-end.
- Bad, because formal intake for a self-evidently necessary plugin is pure ceremony — no real triage decision is being made.
- Bad, because building research tooling as a separate plugin first would delay everything, and that tooling itself would face the same bootstrap problem.

### Full Exemption

- Good, because maximum speed — no process overhead at all.
- Bad, because it provides no validation of any PDLC stage.
- Bad, because "the first plugin is exempt" could easily become "this plugin is special" indefinitely.
- Bad, because it misses the opportunity to retroactively run plugin-authoring through the PDLC it enables.

## More Information

- [plugin-authoring Concept Capture: Bootstrap Exception](../notes-to-process/plugin-authoring-concept.md) — details of the two deviations
- [PDLC: Intake](../development/pdlc.md) — the standard intake process that plugin-authoring bypasses
- [ADR-0005: No Inter-Plugin Dependencies](./0005-no-inter-plugin-dependencies.md) — bundled research capability will be extracted without creating a dependency
