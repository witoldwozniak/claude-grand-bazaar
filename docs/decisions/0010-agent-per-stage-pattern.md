---
title: "ADR-0010: Agent-per-Stage Pattern"
description: "plugin-authoring uses one dedicated agent per PDLC stage."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Agent-per-Stage Pattern

## Context and Problem Statement

plugin-authoring encodes the PDLC as an executable agent chain. Each of the nine PDLC stages (Concept through Tend) involves different skills, tools, and decision boundaries. The plugin needs an architecture that ensures the right context is loaded at each stage without relying on the agent to remember what stage it's in.

How should agents map to PDLC stages?

## Considered Options

1. One dedicated agent per PDLC stage (agent-per-stage pattern)
2. A single generalist agent that loads different skills based on the current stage
3. Agents grouped by phase — one for discovery (Concept/Research/Design), one for execution (Build/Prove/Review/Document/Ship), one for maintenance (Tend)

## Decision Outcome

Chosen option: "One dedicated agent per PDLC stage", because deterministic skill assignment and tool scoping at the agent level guarantees correct context without relying on runtime judgment.

### Consequences

**Good:**

- Each agent has exactly the skills and tools it needs — no more, no less.
- Focus is enforced structurally: the concept agent cannot accidentally start building, the build agent cannot accidentally start documenting.
- Intellectual weight lives in skills; agents provide scaffolding. The separation is clean.
- Consistent pattern makes it easy to understand and extend.

**Bad:**

- Nine agents is a high count for a single plugin.
- Handoff between agents requires a mechanism (user-initiated, command-triggered, or explicit routing).
- Some stages (Ship) are thin enough that a dedicated agent adds more ceremony than value.

## Pros and Cons of the Options

### Agent-per-Stage

- Good, because skill loading is deterministic — the agent's definition specifies exactly which skills it uses.
- Good, because tool scoping is explicit — a research agent has web search tools, a build agent has file editing tools.
- Good, because it mirrors the PDLC's own stage boundaries, making the mapping intuitive.
- Bad, because nine agents means nine agent definition files to maintain.
- Bad, because thin stages (Ship) get a dedicated agent for pattern consistency rather than functional necessity.

### Single Generalist Agent

- Good, because one agent to maintain and understand.
- Bad, because the agent must dynamically determine which skills to load — progressive disclosure is probabilistic rather than deterministic.
- Bad, because tool scoping becomes the agent's responsibility, not its definition's guarantee.
- Bad, because stage boundaries blur when the same agent handles everything.

### Grouped by Phase

- Good, because fewer agents (three) while still maintaining some separation.
- Bad, because each agent handles multiple stages with different needs — the discovery agent must context-switch between concepting, researching, and designing.
- Bad, because the grouping is somewhat arbitrary — Build and Review have less in common than the "execution" label suggests.

## More Information

- [plugin-authoring Concept Capture: Core Architecture](../notes-to-process/plugin-authoring-concept.md) — agent-per-stage definition and stage details
- [PDLC](../development/pdlc.md) — the nine stages that map to agents
- [ADR-0004: Six Primitives Model](./0004-six-primitives-model.md) — agents are one of the six primitives
