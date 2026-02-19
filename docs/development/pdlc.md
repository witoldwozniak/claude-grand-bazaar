---
title: Plugin Development Life Cycle
description: "How a plugin goes from idea to shelf — and how it stays there."
---

# Plugin Development Life Cycle

**Status:** Draft

_How a plugin goes from idea to shelf — and how it stays there._

## Overview

The early stages — Concept, Research, Design — often loop as understanding deepens. The later stages — Build and Prove — are more sequential, though findings during Prove can send you back to Design or Build. Once a plugin ships, it enters Maintenance.

```
Concept → Research ⇄ Design → Build → Prove → Ship → Maintenance
             ↑          ↑                                 |
             └──────────┴─────────────────────────────────┘
```

## Intake

Before a plugin enters the PDLC, it starts as a **Plugin Proposal** — a GitHub Issue using the plugin proposal template. Proposals can come from the community or from ourselves.

Not every proposal becomes a plugin. The proposal template includes a triage checklist — the Proposer answers these questions and the Maintainer evaluates these answers.

Accepted proposals get a **Plugin Tracker** — the living tracker for that plugin's journey through the PDLC. Declined proposals are closed with an explanation.

## Project Management

Each plugin gets one **Plugin Tracker** that tracks its progress. The issue body contains sections for concept, design notes, and evidence from proving. Task lists inside the issue track which stages are done.

**Research** is conducted in a separate **Research Request** issue. Research produces a reference artifact that outlives the plugin's development. A domain study may inform multiple plugins, or serve Bazaar infrastructure that isn't tied to any specific plugin. Research issues stay valuable long after the plugin ships.

Labels handle association and filtering:

- `plugin/<name>` — ties issues, research, and PRs to a specific plugin
- GitHub's default labels (`bug`, `enhancement`, `documentation`, etc.) cover everything else
- Add project-specific labels as needed

Milestones track shipping goals. The v1.0.0 milestone groups everything needed to launch.

## Stages

### 1. Concept

Define the plugin's scope and ambition. This lives as the opening section of the Plugin Issue.

Answer three questions:

- What specific ground does this plugin cover — and what does it deliberately leave out?
- What would success look like when it's on the shelves?
- What are the likely primitives — Skills, Hooks, Subagents, Connectors, LSP servers?

Keep it short. A few paragraphs, not a document. If the concept needs pages of explanation, it's probably too big for one plugin.

### 2. Research

Study the domain. This is where "we study before we sell" lives.

Start with academic papers and published industry research. Then community practice, handled with care. Cast a wide net, select carefully. For Claude Code-specific domains where academia is silent, the community is the frontier.

This stage can take time. That's fine. A merchant who rushes his craft fills his shelves with junk.

Research is documented in its own **Research Request** issue — it's a reference artifact, not just a stage to pass through. When the domain evolves during Maintenance, you'll come back to it.

Done when you understand the domain well enough to form an opinionated view of how things should work. Open questions identified.

### 3. Design

Make the opinionated choices.

- What is the plugin's point of view?
- Which primitives does it need?
- How does it compose with existing plugins?
- What does it deliberately leave out?
- If the plugin uses only Skills, Subagents, and Connectors — note it as Cowork-compatible. If it requires Hooks or LSP servers — note it as Claude Code-only.

Design includes scoping. Not every insight from Research belongs in the plugin. Ruthless selection is part of the craft.

Design decisions go in the Plugin Issue. Significant architectural trade-offs get an ADR when they warrant one.

### 4. Build

Implement the plugin. One PR per unit of work, TDD where it applies, review before merge.

Since plugins are primarily markdown, documentation is an integral part of building. The SKILL.md files, Subagent definitions, hook configs, and the README are all built as part of implementation. When the plugin is built, it's documented.

Before marking Build as done, review what you've built against the Doctrine's quality bar: research-grounded, well-documented, composable, opinionated, tested. Does it stay within its declared scope? Does it do things it said it wouldn't?

### 5. Prove

Use it in real work. Not synthetic tests, not hypothetical scenarios — actual projects with actual problems.

This is where the opinions get tested. Keep a lightweight evidence log in the Plugin Issue:

- Which sessions used the plugin, and on what kind of work
- What worked as designed
- What surprised — positively or negatively
- What had to be worked around
- Specific examples where the plugin produced meaningfully better output than unassisted Claude Code

There's no fixed timeline. It's done when you've seen enough variety to trust the opinions. Minimum bar: the plugin must survive contact with at least one real project that the plugin author didn't design the plugin for.

If the opinion doesn't hold up, go back to Design. If the opinion is sound but the implementation is wrong, go back to Build. These are different failures with different remedies.

#### Shipping

When the plugin is proven, run the shipping checklist:

- [ ] Plugin entry added to `.claude-plugin/marketplace.json`
- [ ] Plugin directory exists at the referenced path
- [ ] All primitives installable and functional from a clean state
- [ ] README passes the stranger test — a stranger can understand what it does, why it exists, and how to use it without asking anyone
- [ ] Fresh install verified — not from the dev environment, but as a stranger would encounter it
- [ ] Cowork compatibility noted in the README
- [ ] Plugin Issue closed

### 6. Maintenance

A plugin's life doesn't end at shipping. The domain evolves, users find problems, and Claude Code ships new capabilities.

Three things trigger action:

- **Bug reports and change requests** — something happened, the plugin needs to respond. Small fixes are standalone issues.
- **Domain evolution** — new research, shifted best practices. No one filed an issue, but the plugin's opinion needs revisiting. Routes back to Research or Design.
- **Platform shifts** — Claude Code ships new primitives or changes existing ones. Routes back to Design.

Not every stall stays open forever. If a domain collapses, a better alternative emerges, or the platform no longer supports what the plugin needs — the plugin gets retired. Sunsetting means removing it from the marketplace manifest and documenting why.
