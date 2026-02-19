---
title: Doctrine
description: "The Grand Bazaar's operational principles — its constitution for quality, composability, and opinionated design."
---

# Claude Grand Bazaar Doctrine

_v0.1 — February 11, 2026_

## What This Is

Claude Grand Bazaar is a plugin marketplace for [Claude Code](https://claude.com/product/claude-code) and [Claude Cowork](https://claude.com/product/cowork). It provides opinionated, research-grounded plugins that extend what Claude can do.

It is both a production tool and a vehicle for discovery. Building top-shelf plugins means understanding the domains they capture — and sometimes uncovering new ways of working with Claude Code that nobody has documented yet. We take our time. We research before we build, and we treat the building as an opportunity to discover, not just ship.

## Ambition

Quality before quantity. We'd rather have five excellent plugins than twenty mediocre ones. Not every idea becomes a plugin. Not every started plugin reaches the shelves. If something isn't meeting the standard, we'd rather hold it back than ship it early.

## Target and Portability

We build for Claude Code. That's the primary target. [Claude Code supports five primitives: Skills, Hooks, Subagents, Connectors, and LSP servers](https://code.claude.com/docs/en/plugins-reference). [Commands were absorbed into Skills](https://github.com/anthropics/claude-code/blob/b757fc9ecdf77e450442e3ca9f9093a9da35952b/CHANGELOG.md#213) — skills now handle both automatic context loading via progressive disclosure and explicit invocation via slash commands. We do not add `commands/` directories to plugins.

Claude Cowork is a secondary target. Its plugin system shares Claude Code's format — same `plugin.json` manifests, same directory structure, same `marketplace.json` catalogs. [Cowork supports three of the five primitives](https://support.claude.com/en/articles/13345190-getting-started-with-cowork#h_0f9e0998dd): Skills, Subagents, and Connectors (MCP servers). It does not support Hooks or LSP servers. Any Bazaar plugin that doesn't depend on Hooks or LSP servers works on Cowork without modification. Since we do not provide slash commands, Cowork users rely on progressive disclosure for skill invocation, or can customize the plugin themselves.

We design for Claude Code's full capability surface. We never weaken a plugin to fit Cowork's subset. But when a plugin naturally fits within the three shared primitives, we note it as Cowork-compatible — extending reach without compromising design.

Portability beyond the Anthropic ecosystem is a courtesy, not a constraint. Plugin content is written in model-agnostic markdown and scripts. But we will never compromise a design decision to accommodate a platform we don't target.

The coding agent landscape moves fast. When the ecosystem converges on common protocols and structures, we can think about ports. Until then, we focus on Claude Code.

## Research-Based Development

We go deep before we build. We prefer vetted knowledge over folk wisdom.

The hierarchy: academic research and published research from industry labs first. Our own experiments and direct experience with Claude Code second — we build plugins daily and discover things no paper covers. Community discoveries and knowledge third, treated with extra caution. We cast a wide net but carefully select what to use.

This principle flexes by domain. For well-established disciplines the literature comes first. For territories where academia is silent, the community _is_ the frontier. The best available source varies; rigor doesn't.

Research serves implementation. We know when to stop reading and start making.

## Opinionated by Design

We ship what we think is right. We don't try to make everyone happy, and we won't hedge our recommendations to avoid disagreement.

Each plugin encodes a specific view of how its domain should work. Users choose which plugins to install — that's the choice point. Once installed, the plugin has opinions, and it doesn't apologize for them.

We welcome constructive criticism and are always open to discussion. But this isn't a wish list — we make deliberate choices about what to build and how, and we'd rather ship something we believe in than something that tries to please everyone.

## Composability

Every plugin works alongside every other plugin without conflict. Nothing is mandatory, but everything must peacefully coexist.
Some plugins cover software engineering disciplines — documentation, testing, project management. Others cover niche domains — game modding, prose writing, newsletter management. The domain doesn't matter. The rule is the same: installing one plugin never breaks another.
This means Hooks don't interfere, Agent roles don't overlap without adding value, and Skills don't contradict each other. Composition is verified and is part of the quality bar.

## The Five Primitives

Plugins [compose from five building blocks](https://code.claude.com/docs/en/plugins-reference#plugin-components-reference). Each has a distinct role:

**Skills** provide knowledge and reasoning guidelines. They load automatically through progressive disclosure when the context calls for them, or explicitly when invoked via slash command. Skills are the most versatile primitive — they shape how Claude thinks about a domain without constraining its tools.

**Hooks** provide event-driven automation — shell scripts and prompts that run in response to Claude Code lifecycle events like pre/post tool use, session start, and notification triggers. If a behavior must happen every time without exception, it belongs in a Hook. The key distinction: Hooks guarantee, Skills suggest.

**Subagents** provide focus. They are subagents with isolated context, constrained tool access, and a declared scope. A Subagent ignores everything outside its domain — an architect Subagent doesn't touch tests, a security Subagent doesn't care about prose. This deliberate narrowing produces better output than giving everything to one general-purpose agent.

**Connectors** (MCP servers) provide external reach — the bridge between Claude and the outside world. They connect to APIs, databases, third-party services, and file systems beyond Claude's native access. Anything Claude needs to touch but can't reach natively goes through a Connector.

**LSP servers** provide real-time code intelligence — diagnostics after every edit, type awareness, navigation through definitions and references. Where Skills carry static knowledge, LSP servers see the living code as it changes.

## On Roles

Roles are useful when they constrain attention. An architect Subagent deliberately ignores implementation detail to think about structure. A test Subagent doesn't worry about documentation style. The constraint is the point.

Roles become harmful when they add ceremony without adding focus — Subagents "discussing" for the appearance of rigor rather than producing better output. The principle: a role must produce meaningfully different output than an unscoped agent would. If it doesn't, remove it.

[Agent teams](https://code.claude.com/docs/en/agent-teams) are orchestration, not simulation. The question is whether the structure produces better work, not whether it looks impressive.

## Human in the Loop

When agents encounter gaps that tooling cannot fill — inaccessible sources, judgment calls requiring domain expertise, permissions they don't have — they flag the need explicitly rather than guessing, inventing, or failing silently. The human is a fallback for anything the agent can describe but cannot reach.

This is a design principle, not a weakness. An agent that says "I need someone to access this paywalled paper and tell me what Section 3 concludes about X" is more useful than one that hallucinates an answer or silently skips the source. Agents should make their needs specific so the human can act efficiently.

## Documentation

Plugins are primarily markdown. The SKILL.md files, Subagent definitions, and README are the product — building a plugin IS writing documentation. There is no truly separate documentation step.

The stranger test: if someone can pick up a plugin and understand what it does, why it exists, and how to use it without asking anyone, the docs are good enough. If they can't, they aren't. Future us are strangers. We write thinking of them.

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

- **Researched.** Core decisions are traceable to vetted sources — academic, published industry research, or (where those don't exist) carefully evaluated community practice.
- **Documented.** A stranger can understand what it does, why it exists, and how to use it without asking anyone.
- **Composable.** It works alongside every other plugin without conflict.
- **Opinionated.** It takes a clear position on how its domain should work. No hedging, no "you could also try…" equivocation.
- **Tested.** It has been used in real work, not just written and published.
