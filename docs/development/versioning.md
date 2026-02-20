---
title: Semantic Versioning
description: "Versioning strategy for plugins and marketplace artifacts, following SemVer 2.0.0."
---

# Semantic Versioning Strategy

_Draft — February 13, 2026_

## Overview

The Grand Bazaar uses [Semantic Versioning 2.0.0](https://semver.org/) for all versioned artifacts. Each plugin is versioned independently. The marketplace manifest is versioned separately from its plugins.

## What Gets Versioned

**Plugins** — each plugin carries its own version number, independent of all other plugins and the marketplace. Users install and update plugins individually; version numbers must be meaningful in isolation.

**Marketplace manifest** — the catalog structure (`marketplace.json`) that describes available plugins, their metadata, and installation mechanics. Bumped only when the catalog format or installation mechanism changes, not when plugin contents change.

## Pre-1.0 and the Quality Gate

Plugins start at `0.1.0` and iterate freely. The `0.x.y` range signals that the plugin is usable but still maturing — research may be ongoing, the approach may shift, and breaking changes can occur without ceremony.

A plugin graduates to `1.0.0` when it meets the quality bar defined in the Doctrine:

- Research-grounded
- Well-documented
- Composable
- Opinionated
- Tested in real work

The `1.0.0` release is a deliberate act, not an automatic milestone. It signals that the plugin's design has stabilized and users can rely on its versioning contract.

## The Hard/Soft Contract Split

Not all primitives have the same kind of interface. The Bazaar distinguishes between hard and soft contracts, which determines how strictly SemVer applies.

### Hard Contracts

**MCP servers, LSP servers, and hooks** have concrete, mechanically verifiable interfaces — protocols, event triggers, matcher patterns, commands, capability negotiations.

Breaking changes are identifiable without judgment calls:

| Primitive  | MAJOR (breaking)                                                | MINOR (additive)                        | PATCH (fix)                      |
| ---------- | --------------------------------------------------------------- | --------------------------------------- | -------------------------------- |
| MCP server | Removed tool, changed request schema                            | New tool, new optional parameter        | Bug fix, performance improvement |
| LSP server | Dropped capability, changed config format                       | New diagnostics, additional LSP feature | Fixed false positive, perf fix   |
| Hook       | Changed event trigger, removed matcher, new required dependency | New matcher, expanded scope             | Regex fix, better error message  |

### Soft Contracts

**Skills and Subagents** have interfaces made of prose consumed by an LLM. There is no type checker, no protocol negotiation, no mechanical way to detect incompatibility. The LLM adapts to changes gracefully, which means nothing breaks loudly.

SemVer here communicates intent to humans, not compatibility to tooling:

| Primitive | MAJOR (scope/intent shift)                                                    | MINOR (additive)                   | PATCH (fix)                       |
| --------- | ----------------------------------------------------------------------------- | ---------------------------------- | --------------------------------- |
| Skill     | Fundamental approach changed, scope redefined                                 | New sections, broader coverage     | Clarified wording, fixed examples |
| Subagent  | Role scope changed, tools removed from allowlist, decision boundaries shifted | New tools added, expanded guidance | Prompt refinement, typo fix       |

Because soft-contract breakage is a judgment call, lean toward MINOR when uncertain. Reserve MAJOR for changes where a user who built workflows around the previous version would be surprised by the new behavior.

## Dependencies

**No inter-plugin dependencies.** Every plugin works in isolation. Plugins may complement each other through careful scoping, but no plugin requires another plugin to function.

If shared behavior emerges between plugins, it is duplicated rather than extracted into a shared dependency. Duplication is cheaper than coupling in a marketplace where users choose their own subset.

**Minimum Claude Code version.** Plugins declare a minimum Claude Code version in their manifest when they rely on platform features (specific hook events, LSP support, etc.).

## Auto-Update and User Trust

Users choose whether to auto-update or pin versions. The Bazaar respects that choice by versioning responsibly:

- Hard-contract MAJOR bumps demand attention — a hook or server changed its behavioral contract.
- Soft-contract MAJOR bumps warrant review — a skill or agent shifted its approach.
- MINOR and PATCH bumps should never require user intervention.

Version numbers are a trust signal. Users on auto-update are trusting that we won't ship a MINOR that's actually a MAJOR. That trust is earned by being honest about what changed.
