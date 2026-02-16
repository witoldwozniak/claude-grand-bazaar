# plugin-authoring — Concept Capture

**Status:** Concept stage complete — triaged and resolved. Ready for Research.
**Date:** 2026-02-15
**Source:** Conversation between witoldwozniak and Claude, discussing PDLC application to plugin-authoring

## Navigation

[What This Plugin Is](#what-this-plugin-is) · [Bootstrap Exception](#bootstrap-exception) · [Core Architecture](#core-architecture-agent-per-stage-pattern) · [Stages](#stages): [/create-plugin](#create-plugin-entry-point) · [Concept](#1-concept) · [Research](#2-research) · [Design](#3-design) · [Build](#4-build) · [Prove](#5-prove) · [Review](#6-review) · [Document](#7-document) · [Ship](#8-ship) · [Tend](#9-tend) · [Summary](#summary) · [Actions](#actions) · [Observations](#observations) · [Open Questions](#open-questions) · [Next Steps](#next-steps)

---

## What This Plugin Is

The Delta Force of the Grand Bazaar. Bootstraps the entire marketplace by encoding the PDLC as an executable agent chain. Built before the doctrine existed — now being retroactively run through the process it enables.

## Bootstrap Exception

This plugin bypasses parts of the standard PDLC because it must exist before the process it encodes can run. Two deviations from normal flow:

- **Implicit intake.** No formal Plugin Request or triage — plugin-authoring is self-evidently necessary as the first plugin. The intake decision was made when the project was conceived.
- **Bundled research capability.** The Research stage agents and skills live inside plugin-authoring because no `domain-research` plugin exists yet. When one is extracted later, plugin-authoring simply drops the bundled tooling. No dependency is created — users compose plugins themselves.

Both deviations are scoped to the bootstrap. Future plugins go through formal intake and use whatever research tooling exists at the time. See [Actions](#actions) for the ADR that records this.

## Core Architecture: Agent-per-Stage Pattern

Each PDLC stage has a dedicated agent acting as a **stage harness**. Agents guarantee correct skills loaded, tools scoped, and focus maintained. Intellectual weight lives in skills; agents provide scaffolding. Progressive disclosure is probabilistic; agent skill assignments are deterministic.

Entry point is `/create-plugin` command → creates GitHub Milestone → hands off to plugin-conceptualizer → linear chain through stages with recognized recursion points.

**Agent handoff:** Each stage is a separate human-initiated session. The finishing agent outputs clear next-step instructions — what was completed, what the next stage is, and what the next agent needs to know. The human starts a new conversation and invokes the next stage. No automated agent chaining; the human is the orchestrator between stages.

All work happens on a working branch (e.g. `plugin/<n>`), created at the start of Concept. Trunk-based development — merge when ready.

---

## Stages

### /create-plugin (Entry Point)

Creates GitHub Milestone (just needs plugin name). Hands off to Concept agent. This step assumes intake has already happened — a Plugin Request was accepted, or (in the bootstrap case) the need is self-evident.

### 1. Concept

**Agent:** `plugin-conceptualizer`

- Creates working branch
- Loads concept skill, scopes tools, ensures focus
- Creates `[concept]` issue with `stage/concept` label via `gh` CLI
- Issue is NOT auto-closed — Code Actual approval gate

**Skills:**

- `concept-scoping` — Guides investigation: scan Claude Code docs for primitives, check GitHub for prior art, read Bazaar doctrine/quality standards, skim PDLC. Produces: domain description, boundary intuitions, landscape scan, rough primitive guesses, success criteria, research questions for next stage.
- `doctrine` — OPEN QUESTION: May not need a separate skill if CLAUDE.md coverage is sufficient. Resolve during Prove.

**Key decisions:**

- Lightweight — mostly a thinking stage, not a building one
- Must produce meaningful research questions as handoff to Research
- `gh` CLI for GitHub, not MCP

**Exit:** Working branch created. Concept issue populated, milestone created, research questions defined. Awaits Code Actual approval.

### 2. Research

**Agent:** `plugin-researcher`

- Single role, multiple parallel instances as teammates
- Tools: Web Search, Read, Bash (gh, doc processing), web_fetch

**Skills:**

- `structured-gathering` — Combined methodology + source processing. Source hierarchy (academic → industry → community). For each source: provenance, proxy credibility signals, relevance to research questions, uncertainties, stability/volatility estimate, what agent couldn't assess. Process as you gather — structured record is primary output.
- `synthesis` — Operates on accumulated corpus after gathering. Identify convergence/contradiction, surface open questions, recognize when you have enough. Iterative: synthesize → identify gaps → gather more → re-synthesize.

**Key decisions:**

- One role is sufficient — method is identical regardless of source type
- Parallelism via multiple instances, not multiple roles
- No hooks — discipline comes from skills and process, not enforcement
- No MCP shipped — Chrome extension is optional user composition
- Depth decision dissolved: go wide, process everything, select during synthesis
- Credibility = proxy signals checklist + honest annotation, not holistic LLM judgment (same problem as agent-skills quality assessment)
- Source volatility recorded — informs Tend stage re-checking
- Inaccessible sources flagged for Code Actual (human as ultimate MCP server)
- Research capability bundled in plugin-authoring for bootstrap; may extract to `domain-research` later without creating dependency (users compose plugins, no inter-plugin dependency)
- `web_fetch` reads pages; Chrome extension adds interaction (SPAs, forms, multi-page navigation)

**Exit:** Research corpus as structured markdown. Research issue documents key sources, opinionated view forming, open questions. Code Actual reviews.

### 3. Design

**Agent:** `plugin-designer`

- Loads all three design skills
- Facilitates dialogue with Code Actual rather than delegating to subprocess

**Skills:**

- `boundary-analysis` — Examine existing marketplace plugins via manifests and trigger patterns. Map claimed territory. Identify available space. Other plugins are hard boundaries — if overlap feels wrong, open an Issue, don't modify.
- `design-facilitation` — Take research synthesis + boundary map, present options to Code Actual. Surface trade-offs explicitly. Scope alternatives from lightweight to heavy. Guide toward exit criteria: opinion, primitives, boundaries.
- `primitive-selection` — When to use each primitive. Skills for reasoning, hooks for enforcement, agents for focused attention, MCP for external connections, LSP for real-time code intelligence. Grounded in Bazaar's primitive docs.

**Key decisions:**

- Other plugins' boundaries are hard constraints, not negotiable
- Design operates within constrained territory: research says what's possible, existing plugins say what's taken

**Exit:** Design issue documents opinion, chosen primitives, boundaries, composition points. Code Actual approves.

### 4. Build

**Agent:** `plugin-builder`

- Loads appropriate primitive-building skills based on design specs
- Design specs define the "what"; Build focuses on "how"
- Follows disciplined cycle: one Issue = one PR, TDD, review gate before merge

**Skills:**

- `skill-building` — How to build skills. Progressive disclosure, SKILL.md conventions, bundled resources.
- `agent-building` — How to build agents. Frontmatter, triggers, tool scoping, model selection, system prompts.
- `hook-building` — How to build hooks. Event types, matchers, hook types (command/prompt/agent), interference testing.
- `mcp-building` — How to build MCP servers. Thinner initially — less explored territory. Anthropic's published examples inform it.
- `lsp-building` — How to build LSP servers. Thinner initially — less explored territory.

**Key decisions:**

- One agent, five primitive-specific skills
- MCP and LSP skills may ship thinner — acceptable, grows during Tend
- Existing plugin-authoring agents (agent-creator, hook-author, plugin-builder, etc.) are fully replaced by agent-per-stage pattern
- Composition with existing core plugins verified during Build, not deferred to Review

**Exit:** Working plugin, all primitives implemented, tests passing, no known composition conflicts. Build issue closed.

### 5. Prove

**Agent:** `plugin-prover`

- Loads evidence analysis skill
- Reads preprocessed conversation evidence
- Does retrospective analysis, not the proving itself — Code Actual proves by using the plugin in real work

**Skills:**

- `evidence-analysis` — Methodology for comparing expectations against reality. What was designed vs what happened. Diagnostic: opinion doesn't hold → route to Design; implementation wrong → route to Build.
- `evidence-preprocessing` — Convention/script for reducing raw JSONL to conversational skeleton on retrieval. Strips tool payloads, system prompts, raw file contents — keeps human turns, assistant reasoning, tool names, outcomes. Cuts token cost.

**Hook:**

- `session-capture` — SessionEnd hook. Persists conversation JSONL to evidence directory. Mechanical, automatic, no interruption.

**Key decisions:**

- Capture raw JSONL at SessionEnd, preprocess on retrieval, analyze reduced form
- Plugin-authoring proves itself recursively — evidence is the trail of other plugins going through PDLC
- No fixed timeline — done when Code Actual has seen enough variety

**Entry:** A working plugin from Build. Code Actual approves proving approach — which projects, what to look for.

**Exit:** Evidence log documents specific examples. Gap analysis complete. Code Actual satisfied with sufficient evidence to proceed to Review. Prove issue closed.

### 6. Review

**Agent:** `plugin-reviewer`

- Runs review process against design specs and doctrine

**Skills:**

- `review-checklist` — Lightweight guide. Structural validation, doctrine compliance, design spec fulfillment, composition check. Distinguishes auto-pass/fail (structural, mechanical — automated via scripts) from flags for Code Actual (qualitative concerns, ambiguous composition, low-confidence assessments). Diagnostic for routing findings to Design vs Build.

**Key decisions:**

- Self-review for now
- No documentation review — that's Document stage
- Structural checks automated via scripts
- Review issue arrives with clear sections: passed, failed, needs your judgment

**Exit:** Findings acceptable. Review issue closed. Code Actual approves.

### 7. Document

**Agent:** `plugin-documenter`

- Loads documentation skills

**Skills:**

- `plugin-docs` — How to write plugin documentation. README structure, per-primitive docs patterns, standalone requirement, stranger test criteria.
- `docs-site-template` — Consistent template for docs site reference pages (`content/en/`). Component-library style: description, primitives list, configuration, usage, opinions. Navigational consistency across marketplace.
- `write-for-llms` — Write precise prose optimized for LLM consumption. Carried forward from current plugin-authoring.

**Key decisions:**

- Plugin ships README only — hand-written, covers what/why/install/usage/opinion (see [ADR-0014](../decisions/0014-documentation-architecture.md))
- Primitives are self-documenting: SKILL.md frontmatter, agent .md frontmatter, hook configs ARE the primitive docs
- Research/design notes live externally (GitHub Issues are canonical; marketplace site assembles views programmatically)
- README passes stranger test independently
- Docs site pages follow consistent template like component library references
- Broader documentation tooling deferred to future `documentation-authoring` plugin

**Exit:** README present and passes stranger test. Primitive metadata complete in structured files. Document issue closed.

### 8. Ship

**Agent:** `plugin-shipper`

- Thin agent for pattern consistency — checklist execution

**Steps:** Merge branch to trunk → update marketplace.json → run CI → verify fresh install from clean state → close all stage Issues (Concept through Ship) → close milestone

**Key decisions:**

- Mostly mechanical — agent exists for consistency, not intellectual weight
- Fresh install verification is critical — catches dev environment assumptions
- Code Actual gives final approval before merge

**Exit:** Plugin installable and discoverable. Manifest updated. Branch merged. CI green. Fresh install verified. All stage Issues (Concept through Ship) and milestone closed. No Tend issue opened — maintenance is free-standing (see [ADR-0013](../decisions/0013-milestone-lifecycle.md)).

### 9. Tend

**Agent:** `plugin-tender`

- Triages incoming triggers
- Routes to appropriate action

**Skills:**

- `maintenance-triage` — Decision framework: bug fix or small tweak → free-standing maintenance issue, stays in Build scope. Domain evolution or platform shift requiring opinion rethinking → new milestone, re-enters PDLC at Research or Design.

**Key decisions:**

- Plugin milestone closes at Ship — milestones represent bounded work
- Maintenance issues are free-standing, labeled `stage/maintenance` + `plugin/<n>`
- Enhancements that route back to Research or Design spawn new milestones
- "Tend" in PDLC prose, "maintenance" in project management labels
- Sunsetting path exists

**Exit:** No exit — ongoing. Leaves only through sunsetting.

---

## Summary

|                 | Count                                              |
| --------------- | -------------------------------------------------- |
| Agents          | 9 (one per stage + entry command)                  |
| Skills (unique) | ~16 (doctrine counted once, pending open question) |
| Hooks           | 1 (session-capture)                                |

---

## Actions

- [x] Write ADR: Bootstrap Exception → [ADR-0011](../decisions/0011-bootstrap-exception.md)
- [x] Write ADR: Agent-per-Stage Pattern → [ADR-0010](../decisions/0010-agent-per-stage-pattern.md)
- [x] Write ADR: Milestone Lifecycle & Maintenance → [ADR-0013](../decisions/0013-milestone-lifecycle.md)
- [x] Build: ADR index auto-generation in CI pipeline — CI validates freshness; `scripts/index-decisions.py` exists

## Observations

- **Plugin Contract Problem** — Plugins lack formal contracts. Boundaries declared via prose with no enforcement. Known platform limitation.
- **Human as Ultimate MCP Server** — Code Actual fills gaps tooling cannot. Agents flag needs and receive input. Added to [Doctrine](../doctrine.md).
- **/create-plugin Command Flow** — Linear agent chain with recursion points. Documented in plugin docs.

## Open Questions (Resolved)

- **Q1: Doctrine: Skill vs CLAUDE.md** — Deferred. Resolve during Prove — may not need a separate doctrine skill if CLAUDE.md coverage is sufficient.
- **Q2: Document stage artifacts** — Resolved. PDLC updated: plugin ships README only; primitives self-documenting via structured files; research/design notes external. See [ADR-0014](../decisions/0014-documentation-architecture.md).
- **Q3: No Code Actual checkpoint after Prove** — Resolved. PDLC is correct — checkpoint exists. Prove exit in this document updated to include Code Actual approval.
- **Q4: Prove entry condition underspecified** — Resolved. PDLC is correct — proving approach agreement exists. Prove entry in this document updated to include Code Actual approval of approach.
- **Q5: Review is lighter than published PDLC** — Resolved. Review kept lighter: quality bar, composition, boundary check, platform check. Stranger test lives in Document only. Opinion coherence implicit in design spec fulfillment. PDLC updated to match.
- **Q6: Agent handoff mechanism** — Resolved. Each stage is a separate human-initiated session. Finishing agent outputs clear next-step instructions; human invokes next stage. Documented in Core Architecture section above.
- **Q7: Tend issue lifecycle at Ship** — Resolved. No persistent Tend issue. Milestone closes at Ship. Maintenance issues are free-standing. See [ADR-0013](../decisions/0013-milestone-lifecycle.md).
- **Q8: SDLC relationship** — Resolved. All SDLC references removed from PDLC. SDLC is a domain doc mapping future core plugins — it does NOT define the Bazaar's own development process. Plugin authoring follows PDLC only.
- **Q9: Research questions not captured** — Resolved. Research questions added below.

---

## Research Questions

The Concept stage's primary deliverable — the questions that Research will investigate.

### Platform & Primitives

- What are the current capabilities and constraints of each Claude Code primitive (skills, hooks, agents, MCP, LSP, commands)? What's documented vs discovered?
- How do agent frontmatter fields (model, tools, skills, hooks, maxTurns) affect behavior in practice? What are the effective limits?
- What evidence exists for optimal skill structure — size, progressive disclosure patterns, reference organization?

### Agent Design

- What makes an agent produce "meaningfully different output" from an unscoped agent? What research exists on role-constrained LLM behavior?
- How should agent instructions be structured for stage-specific focus? What's the relationship between instruction length and adherence?

### Evidence & Proving

- What approaches exist for capturing and analyzing conversation evidence? What preprocessing reduces tokens while preserving signal?
- What constitutes "sufficient evidence" in software tool evaluation? How do existing frameworks (A/B testing, case study methodology) apply?

### Documentation

- What makes documentation effective for LLM consumption vs human consumption? Where do the needs diverge?
- What patterns exist for programmatic documentation assembly from structured source files?

### Composition & Boundaries

- How do existing plugin/extension ecosystems handle boundary declaration and conflict detection?
- What formal or semi-formal approaches exist for declaring plugin contracts?

---

## Next Steps

Continue with Research stage for plugin-authoring itself. This conversation completed the Concept stage — the next session should pick up from "Concept approved, entering Research" and investigate the research questions above.
