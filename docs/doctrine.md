---
title: Doctrine
description: "The Grand Bazaar's operational principles — its constitution for quality, composability, and opinionated design."
navigation:
  icon: i-lucide-scroll-text
---

# Claude Grand Bazaar Doctrine

*v0.1 — February 11, 2026*

## What This Is

Claude Grand Bazaar is a plugin marketplace for Claude Code. It provides opinionated, research-grounded plugins that extend what Claude can do — how it reasons, what it enforces, where it focuses attention, what it sees in living code, and what systems it reaches.

It is both a production tool and a vehicle for discovery. Building top-shelf plugins means understanding the domains they capture — and sometimes uncovering new ways of working with Claude Code that nobody has documented yet. We take our time. We research before we build, and we treat the building as an opportunity to discover, not just ship.

## Scope

Quality before quantity. We'd rather have five excellent plugins than twenty mediocre ones. Not every idea becomes a plugin. Not every started plugin reaches the shelves. If something isn't meeting the standard, we'd rather hold it back than ship it early.

## Target and Portability

We build for Claude Code. That's the primary target — all six primitives, full lifecycle hooks, LSP integration.

Cowork is a secondary target. Its plugin system shares Claude Code's format — same `plugin.json` manifests, same directory structure, same `marketplace.json` catalogs. Cowork supports four of our six primitives: Skills, Agents, MCP servers, and Commands. It does not support Hooks or LSP servers. Any Bazaar plugin that doesn't depend on hooks or LSP works on Cowork without modification.

We design for Claude Code's full capability surface. We never weaken a plugin to fit Cowork's subset. But when a plugin naturally fits within the four shared primitives, we note it as Cowork-compatible — extending reach without compromising design.

Portability beyond the Anthropic ecosystem is a courtesy, not a constraint. Plugin content is written in model-agnostic markdown and scripts. But we will never compromise a design decision to accommodate a platform we don't target.

The coding agent landscape moves fast. When the ecosystem converges on common protocols and structures, we can think about ports. Until then, Claude Code is the workshop and Cowork is the neighboring stall.

## Research-Based Development

We go deep before we build. We prefer vetted knowledge over folk wisdom.

The hierarchy: academic research and published research from industry labs first. Community discoveries second, treated with extra caution. We cast a wide net but carefully select what to use.

This principle flexes by domain. For well-established disciplines — TDD, debugging methodology, code review — the literature comes first. For Claude Code-specific mechanics like hooks, where academia has nothing to say, the community *is* the frontier. The best available source varies; rigor doesn't.

Research serves building. We know when to stop reading and start making.

## Opinionated by Design

We ship what we think is right. We don't try to make everyone happy, and we won't hedge our recommendations to avoid disagreement.

Each plugin encodes a specific view of how its domain should work. Users choose which plugins to install — that's the choice point. Once installed, the plugin has opinions, and it doesn't apologize for them.

We welcome constructive criticism and are always open to discussion. But this isn't a wish list — we make deliberate choices about what to build and how, and we'd rather ship something we believe in than something that tries to please everyone.

## Composability

Everything is made to work well together, but nothing is mandatory.

The Bazaar has two kinds of offerings. **Core plugins** cover software engineering disciplines — plugin authoring, documentation, testing, project management, frontend, backend, database administration, and so on. These are designed as a coherent system where every plugin composes cleanly with every other. **Standalone plugins** are self-contained — a Minecraft modding plugin, a newsletter manager, a prose writing toolkit. Built to the same quality standards, but with no obligation to integrate with the core or each other.

## The Six Primitives

Plugins compose from six building blocks. Each has a distinct role:

**Skills** inform. They carry knowledge and reasoning — how to think about a problem, what to know, what steps to follow. Skill categories include docs-as-skill, workflows, conventions, and reasoning frameworks. These are tags that communicate intent and guide form, not rigid templates.

**Hooks** enforce. They are automated guardrails that run whether the agent remembers to or not. If a behavior must happen every time, it belongs in a hook.

**Agents** focus. They are the master craftsmen of the Bazaar — each one works a single trade with their own tools and skills. An architect agent doesn't dabble in testing. A security agent doesn't care about your prose. The craft earns the focus, and the focus earns the output.

**MCP servers** connect. They provide external reach — connections to tools, APIs, and systems outside Claude's native capabilities.

**LSP servers** perceive. They provide real-time code intelligence — diagnostics after every edit, type awareness, navigation through definitions and references. Where skills carry static knowledge, LSP servers see the living code as it changes.

**Commands** invoke. They are user-initiated entry points — markdown files that become slash commands, loading specific instructions and workflows on demand. Where skills activate automatically based on context, commands activate because a human asked.

Skills for reasoning, hooks for enforcement, agents for focus, MCP servers for connection, LSP servers for perception, commands for invocation.

## On Roles and Theater

Roles are useful when they constrain attention. An architect agent isn't cosplaying — it's a craftsman that deliberately ignores implementation detail to think about structure. The theatrics become harmful when they add ceremony without adding focus, or when agents "discuss" things for the appearance of rigor rather than producing better output.

The principle: roles must earn their existence by producing meaningfully different output than an unscoped agent would.

Agent teams — where a lead coordinates specialized teammates working in parallel — are legitimate orchestration, not simulation. The question is always whether the structure produces better work, not whether it looks impressive.

## Human as Ultimate MCP Server

When agents encounter gaps that tooling cannot fill — inaccessible sources, judgment calls requiring domain expertise, permissions they don't have — they flag the need for Code Actual rather than failing silently or inventing answers. The human is the ultimate fallback integration: any system the agent can describe, the human can reach. Agents should make their needs explicit and specific so the human can act efficiently.

This is not a weakness in the system. It's a design principle. An agent that says "I need someone to access this paywalled paper and tell me what Section 3 concludes about X" is more useful than one that guesses, hallucinates, or silently skips the source. The quality bar demands research-grounded work — and sometimes the ground is only reachable through a human.

## Documentation

Future us are strangers to us now. We treat them like ones.

Every plugin, every skill, every design decision is documented for someone with no context. If a stranger can walk into the Bazaar, pick up a plugin, and understand what it does, why it exists, and how to use it without asking anyone — the docs are good enough. If they can't, they aren't.

## Community

The Grand Bazaar is open and craves the hum of a crowd. Discuss, complain, praise, ask, request, challenge, suggest. The stalls are better for it.

We supply the first batch — the plugins we believe should exist based on our own research and experience. Beyond that, if people buy, we sell. Community demand is a legitimate signal for what to build next. We don't build in isolation and we don't pretend to know every domain worth covering.

Direct contributions will be welcomed through a structured process when the Bazaar reaches v1.0. Until then, we accept feedback through Discussions, bug reports and change requests on individual plugins, and plugin requests for entirely new offerings.

## What This Is Not

**Not an RPG.** Roles serve function, not fantasy.

**Not an AGI scaffold.** We don't promise self-evolving intelligence or autonomous systems that improve themselves.

**Not a vibe coding enabler.** The plugins make deliberate work better, not mindless work possible.

**Not set-and-forget automation.** A human is in the loop, making decisions. The plugins make the agent better at its job. They don't replace judgment.

**Not a universal toolkit.** We build for the Anthropic ecosystem — Claude Code primarily, Cowork where plugins fit naturally. We don't chase compatibility with every coding agent on the market.

## Quality Bar

A plugin is ready to ship when it meets all of the following:

- **Research-grounded.** Core decisions are traceable to vetted sources — academic, published industry research, or (where those don't exist) carefully evaluated community practice.
- **Well-documented.** A stranger can understand what it does, why it exists, and how to use it without asking anyone.
- **Composable.** It works alongside every other plugin without conflict.
- **Opinionated.** It takes a clear position on how its domain should work. No hedging, no "you could also try…" equivocation.
- **Tested.** It has been used in real work, not just written and published.
