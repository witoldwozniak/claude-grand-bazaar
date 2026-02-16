---
title: "ADR-0001: Plugin Language Policy"
description: "Use English for all plugin internals — skills, agents, hooks, and documentation."
status: accepted
date: 2026-02-13
decision-makers:
  - witoldwozniak
---

# Use English for All Plugin Internals

## Context and Problem Statement

Plugins contain skills, agent prompts, hook scripts, and documentation — all of which are consumed by Claude as reasoning scaffolding. Some research suggests that prompting LLMs in different languages can produce qualitatively different outputs, occasionally outperforming English on specific tasks <!-- TODO(claude): needs citation -->. Should we leverage this by writing parts of plugins in other languages (e.g., Polish for certain reasoning patterns), or standardize on English throughout?

A secondary question: should plugins include internationalized variants for users who interact with Claude Code in non-English languages?

## Considered Options

1. English only for all plugin internals
2. Strategic multilingual prompting — use non-English languages where research suggests better performance
3. Internationalized plugin variants — ship translated versions of skills and prompts

## Decision Outcome

Chosen option: "English only for all plugin internals", because the alternatives optimize for behavioral quirks rather than stable foundations, and Claude Code already handles user-language adaptation without plugin involvement.

### Consequences

**Good:**

- Maximum model performance — Claude's instruction following and reasoning are strongest in English.
- Composability — no translation boundaries between plugins that need to work together.
- Community accessibility — contributors worldwide can read, debug, and extend plugins.
- Stability — no dependency on multilingual performance characteristics that may shift between model versions.

**Bad:**

- Forecloses potential marginal gains from language-specific prompting on certain task types.
- User-facing marketplace descriptions remain English-only until community translations emerge post-v1.0.

## Pros and Cons of the Options

### English Only

- Good, because it aligns with the model's strongest capabilities.
- Good, because open-source contributors expect English codebases.
- Good, because composability requires a single reasoning language across the plugin graph.
- Bad, because it leaves potential multilingual performance gains on the table.

### Strategic Multilingual Prompting

- Good, because research shows non-English prompts can sometimes produce different (occasionally better) outputs.
- Bad, because the effect is inconsistent, task-dependent, and not guaranteed across model versions — optimizing for an accident.
- Bad, because it creates debugging complexity when a skill written in Polish behaves differently than expected.
- Bad, because it contradicts the project's principle of shipping deliberate, stable choices over clever tricks.

### Internationalized Plugin Variants

- Good, because it would serve non-English-speaking users more directly.
- Bad, because Claude already responds in the user's language regardless of the plugin's internal language — the pipeline works without translation.
- Bad, because maintaining parallel translations of every skill and prompt creates significant maintenance burden for negligible benefit.
- Bad, because translation drift between variants would cause behavioral inconsistencies.

## More Information

Claude's language handling means plugin internals and user-facing interaction are decoupled: a user writes in Polish, Claude reasons through English-language skills, and responds in Polish. Plugins are scaffolding for the model's reasoning, not direct user communication.

User-facing documentation (READMEs, marketplace descriptions) is a separate concern appropriate for community translation efforts post-v1.0.
