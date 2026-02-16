---
title: Plugin Development Life Cycle
description: "How a plugin goes from idea to shelf — and how it stays there. Nine stages from Concept to Maintenance."
---

# Plugin Development Life Cycle

**Status:** Draft

_How a plugin goes from idea to shelf — and how it stays there._

## Overview

The PDLC is not strictly linear. The early stages — Concept, Research, Design — often loop as understanding deepens. That's expected. Discovery doesn't follow a schedule.

The later stages — Build, Prove, Review, Document, Ship — are more sequential, though findings during Prove or Review can send you back to Design or Build.

Once a plugin ships, it enters Maintenance — the ongoing stage where it lives on the shelves and responds to the world changing around it. Maintenance can route a plugin back to Research (domain evolution) or Design (platform shifts, scope rethinking) when the need arises.

```
Concept → Research ⇄ Design → Build → Prove → Review → Document → Ship → Maintenance
             ↑          ↑                                                    |
             └──────────┴────────────────────────────────────────────────────┘
```

## Intake

Before a plugin enters the PDLC, it starts as a **Plugin Proposal** — a GitHub Issue using the plugin proposal template. Requests can come from the community or from ourselves.

Not every proposal becomes a plugin. Triage evaluates:

- Is this domain complex enough to warrant a plugin, or would a CLAUDE.md snippet suffice?
- Does it align with the Bazaar's scope and quality standards?
- Is it a core plugin or a standalone stall?
- Do we have the knowledge or willingness to study this domain properly?

Accepted requests become a milestone. Declined requests are closed with an explanation.

## Project Management

Each accepted plugin is a **GitHub Milestone**. Each PDLC stage is an **Issue** within that milestone.

```
Milestone: documentation-authoring
  ├── [concept] documentation-authoring
  ├── [research] documentation-authoring
  ├── [design] documentation-authoring
  ├── [build] documentation-authoring
  ├── [prove] documentation-authoring
  ├── [review] documentation-authoring
  ├── [document] documentation-authoring
  └── [ship] documentation-authoring
```

Stage issues use labels: `stage/concept`, `stage/research`, `stage/design`, `stage/build`, `stage/prove`, `stage/review`, `stage/document`, `stage/ship`.

Closing an issue means the stage's exit criteria are met. Closing the milestone means the plugin is on the shelves. After Ship, maintenance issues are free-standing — labeled `stage/maintenance` + `plugin/<name>` — and don't belong to the original milestone. See [ADR-0013](../decisions/0013-milestone-lifecycle.md).

Research issues are particularly valuable as closed artifacts — they contain the domain study that informed the plugin and serve as reference material long after the plugin ships.

## Stages

### 1. Concept

Define the plugin's scope and ambition.

**Entry:** An accepted plugin request.

**Exit:** A clear answer to:

- What specific ground does this plugin cover — and what does it deliberately leave out?
- What would success look like when it's on the shelves?
- What are the likely primitives — skills, hooks, agents, MCP servers, LSP servers, commands?

Documented in the Concept Issue. Code Actual has approved the concept before Research begins.

### 2. Research

Study the domain. This is where "we study before we sell" lives.

Start with academic papers and published industry research. Then community practice, handled with care. Cast a wide net, select carefully. For Claude Code-specific domains where academia is silent, the community is the frontier.

This stage can take time. That's fine. A merchant who rushes his craft fills his shelves with junk.

**Entry:** A concept worth pursuing, approved by Code Actual.

**Exit:** Enough understanding of the domain to form an opinionated view of how it should work. Key sources documented in the Research Issue. Open questions identified.

### 3. Design

Make the opinionated choices.

- What is the plugin's point of view?
- Which primitives does it need — skills, hooks, agents, MCP servers, LSP servers, commands?
- If it's a core plugin, how does it compose with the rest? What integration points exist with other core plugins, and are there potential composition conflicts?
- What does it deliberately leave out?
- If the plugin uses only Skills, Agents, MCP servers, and Commands — note it as Cowork-compatible. If it requires Hooks or LSP servers — note it as Claude Code-only.

Design includes scoping. Not every insight from Research belongs in the plugin. Ruthless selection is part of the craft.

**Entry:** Sufficient domain understanding from Research.

**Exit:** A design that names the plugin's opinion, its primitives, its boundaries, and its integration points with the core. Documented in the Design Issue. Code Actual has approved the design before Build begins.

### 4. Build

Implement the skills, hooks, agents, MCP servers, LSP servers, and commands.

Build follows a disciplined cycle: one Issue = one PR, TDD (red-green-refactor) as the implementation approach, review gate before merge.

What building each primitive involves:

- **Skills** — Distill research into actionable markdown guidance. Structure the knowledge so it changes how the agent reasons, not just what it knows.
- **Hooks** — Implement scripts and configure triggers. Test that hooks fire reliably and don't interfere with each other or with hooks from other plugins.
- **Agents** — Define the role, scope the tools, assign the skills. If the agent is part of a team, configure orchestration.
- **MCP servers** — Implement the server, integrate with external APIs, handle authentication and error cases. Test the connection end-to-end.
- **LSP servers** — Implement language server protocol support, define diagnostic rules, wire up navigation and references.
- **Commands** — Write the markdown, name the file, test the invocation. Verify the command loads the right instructions and the variables resolve correctly.

For core plugins, verify composition with existing core plugins during Build. Catching conflicts here is cheaper than discovering them at Review.

**Entry:** A settled design with primitives identified and boundaries drawn. Code Actual has approved the design.

**Exit:** A working plugin that can be installed and used. All primitives implemented, tests passing, no known composition conflicts with existing core plugins.

### 5. Prove

Use it in real work. Not synthetic tests, not hypothetical scenarios — actual projects with actual problems. The project should be one where the plugin's domain is genuinely needed, not a sandbox contrived to validate it.

This is where the opinions get tested. Keep a lightweight evidence log:

- Which sessions used the plugin, and on what kind of work
- What worked as the design inMaintenanceed
- What surprised — positively or negatively
- What had to be worked around
- Specific examples where the plugin produced meaningfully better output than unassisted Claude Code

There's no fixed timeline for Prove. It's done when Code Actual has seen enough variety of situations to trust the opinions. A plugin covering a broad domain needs more proving than a narrow one. Minimum bar: the plugin must survive contact with at least one real project that the plugin author didn't design the plugin for.

If the plugin's opinion doesn't hold up in practice, it goes back to Design — the opinion needs rethinking. If the opinion is sound but the implementation is wrong, it goes back to Build. These are different failures with different remedies.

**Entry:** A working plugin from Build. Code Actual has approved a proving approach — which projects, what to look for.

**Exit:** Confidence that the plugin produces meaningfully better output in its domain. Evidence log documents specific examples. Code Actual is satisfied the plugin has been tested against sufficient variety.

### 6. Review

Self-review for now. Examine the plugin through structured lenses:

- **Quality bar** — Does it meet all five criteria from the Doctrine? Research-grounded, well-documented, composable, opinionated, tested in real work.
- **Composition** (core plugins) — Install alongside all existing core plugins. Do any conflicts arise? Do any hooks interfere? Do any agent roles overlap without adding value?
- **Boundary check** — Does the plugin stay within its declared scope? Does it do things it said it wouldn't? Does it leave gaps in things it said it would cover?
- **Platform check** — If the plugin was designed as Cowork-compatible, verify it contains no hook or LSP dependencies. If it was designed as Claude Code-only, ensure the documentation says so.

Review has three outcomes: **pass** to Document, **return to Build** for implementation issues, or **return to Design** if the opinion or scope needs rethinking.

When the community grows, this stage should include feedback from subject matter experts.

**Entry:** A proven plugin with evidence log.

**Exit:** Confidence that the plugin is ready for a stranger to use. Review findings documented. Any issues resolved or explicitly accepted as known limitations.

### 7. Document

Write for the stranger. Documentation follows the single-source-of-truth principle — see [ADR-0014](../decisions/0014-documentation-architecture.md).

**What ships with the plugin:**

- **README** — What the plugin does, its opinion, how to install, how to use. Hand-written. This is the one artifact where human craft matters.

**What's already documented by structure:**

- **Primitive documentation** — SKILL.md frontmatter, agent markdown frontmatter, hook configs. These structured files ARE the primitive documentation. No separate per-primitive READMEs needed.

**What lives externally:**

- **Research and design notes** — GitHub Issues are the canonical record. The Research Issue contains the full domain study; the Design Issue contains the opinion and trade-offs. Distilled summaries may appear on the marketplace site, but they don't ship inside the plugin directory.

The README must pass the stranger test. A stranger should be able to read it and understand what the plugin does, why it exists, and how to use it without asking anyone.

**Entry:** A reviewed plugin.

**Exit:** README present and passes the stranger test. Primitive metadata complete in structured files.

### 8. Ship

Put it on the shelves.

Shipping checklist:

- Add the plugin entry to `.claude-plugin/marketplace.json` — name, source, description
- Verify the plugin directory exists at the path referenced by `pluginRoot`
- Verify all primitives are installable and functional from a clean state
- Close all stage Issues (Concept through Ship) and close the milestone
- Note Cowork compatibility status in the plugin's README — either "Works on Claude Code and Cowork" or "Requires Claude Code (uses Hooks/LSP)"

After shipping, verify the plugin works when installed fresh — not from the development environment, but as a stranger would encounter it. This catches assumptions that only hold on the author's machine.

**Entry:** A documented, reviewed, proven plugin. All stage Issues (Concept through Document) are closed.

**Exit:** The plugin is installable and discoverable in the Grand Bazaar. Marketplace manifest updated. Milestone closed. Fresh install verified. Code Actual has given final approval.

### 9. Maintenance

A plugin's life doesn't end at Ship. The domain evolves, users find problems, and Claude Code ships new capabilities. Maintenance is the stage where a shipped plugin responds to the world changing around it.

Three things trigger action during Maintenance:

- **Bug reports and change requests** — Users find problems or want improvements. These are reactive: something happened, the plugin needs to respond. Bug fixes and small changes are free-standing issues in Build scope.
- **Domain evolution** — New research is published, best practices shift, the field moves. These are proactive: no one filed an issue, but the plugin's opinion needs revisiting. Domain shifts route back to Research or Design, depending on severity.
- **Platform shifts** — Claude Code ships new primitives, changes how existing ones work, or opens new capabilities. These are adaptive: the plugin may need to take advantage of new tools or adjust to changed behavior. Platform shifts route back to Design.

When a trigger is significant enough to warrant re-entering the PDLC, the plugin routes to the appropriate stage. A bug goes to Build. A shifted opinion goes to Research or Design. A new primitive goes to Design. The plugin then moves forward through the stages again from that point.

Not every stall stays open forever. If a domain collapses, a better alternative emerges, or the platform no longer supports what the plugin needs — the plugin gets retired. Sunsetting means removing it from the marketplace manifest and documenting why it was retired.

**Entry:** A shipped plugin on the shelves.

**Exit:** Maintenance has no exit — it is ongoing for the life of the plugin. A plugin leaves Maintenance only through sunsetting.

## Code Actual Checkpoints

The human decision points across the PDLC, collected in one place:

| Stage              | Decision                                             |
| ------------------ | ---------------------------------------------------- |
| After Concept      | Approve the concept before Research begins           |
| After Design       | Approve the design before Build begins               |
| During Build       | Per-issue merge decisions via review gate            |
| After Prove        | Sufficient evidence to proceed to Review             |
| After Review       | Findings acceptable, proceed to Document             |
| At Ship            | Final approval before the plugin reaches the shelves |
| During Maintenance | Approve re-entry scope when triggers are detected    |
