---
title: Research Guidelines
description: "How research works in the Grand Bazaar — conventions, quality bar, and process."
---

# Research Guidelines

## File Convention

One file per research question. Lives in `./docs/research/`.

Filename format: `YYYY-MM-DD-slug.md` — date is when research began, slug is the question in 2-4 words.

Examples:

- `2026-02-10-hooks-execution-model.md`
- `2026-02-04-epistemic-scaffolding.md`
- `2026-02-12-bundled-focal-models.md`

The template for new research documents is at `docs/research/_TEMPLATE.md`.

## Definition of Done

A research document is **concluded** when all of the following hold:

1. **Question answered.** The Conclusions section directly addresses the question stated in the front matter. "We need more research" is not a conclusion — it's a scope expansion that needs its own research file.

2. **Scope honored.** The document covers what Scope & Constraints promised, nothing less. Covering more is fine if it emerged naturally.

3. **Method documented.** A skeptical reader can evaluate _how_ you reached your findings, not just _what_ you found. Sources are cited. Search strategy is explicit.

4. **Limitations stated.** At least one limitation is named. If you can't think of one, you haven't looked hard enough.

5. **Claims sourced.** Every factual claim either has a citation or is explicitly marked as inference/opinion. No unmarked speculation.

6. **Peer-reviewable.** Someone unfamiliar with the topic can follow the argument from Motivation through Conclusions without needing to ask you what you meant.

7. **Actionable.** The research connects back to a decision, design, or understanding. Pure knowledge accumulation without a use is a wiki article, not project research.

A document is **stale** when its conclusions may no longer hold due to upstream changes (new tool versions, new documentation, shifted project goals). Stale documents should be re-evaluated or archived, not silently trusted.

## What Deserves a Research File?

Not everything. Quick lookups, one-off questions answered in a conversation, and "how do I do X" problems are not research — they're support. Research is warranted when:

- The answer isn't obvious and requires consulting multiple sources
- The findings will inform a design decision or ADR
- You expect to reference the answer again later
- The question has enough depth that you might get it wrong on first pass

## On Academic Rigor

Borrow the discipline, skip the ceremony:

- **Do** state your question precisely before investigating
- **Do** document your method so findings are auditable
- **Do** distinguish evidence from inference from opinion
- **Do** name limitations honestly
- **Don't** write a standalone literature review section (weave sources into Findings)
- **Don't** aim for false objectivity — if you're researching to make a decision, say so
- **Don't** over-formalize language; clear beats impressive

## On Scope Creep

Research expands. You start investigating hooks and end up in the execution model of Claude Code's process isolation. When this happens:

1. Note the tangent in your current document's Limitations or Findings
2. File a new research question if it's worth pursuing
3. Do not let the current document bloat to cover both

## On AI-Assisted Research

When Claude (or any LLM) is a research tool:

- Treat LLM output as a **lead**, not a **source**. Follow claims back to primary sources before citing them.
- Document when findings came from LLM-assisted search vs. direct source review.
- Be especially skeptical of LLM-generated technical details — the "plausible-but-wrong" problem is real and well-documented in your own project history.
- Record the queries/prompts used, just as you'd record search terms.
