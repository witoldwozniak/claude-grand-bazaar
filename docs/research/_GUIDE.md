# Research Guidelines

Template for new research documents: [`_TEMPLATE.md`](./_TEMPLATE.md).

## File Convention

One file per research question. Lives in `./docs/research/`.

Filename format: `YYYY-MM-DD-slug.md` — date is when research began, slug is
the question in 2-4 words.

Examples:

- `2026-02-10-hooks-execution-model.md`
- `2026-02-04-epistemic-scaffolding.md`
- `2026-02-12-bundled-focal-models.md`

### Front matter fields

| Field         | Required | Description                                                    |
| ------------- | -------- | -------------------------------------------------------------- |
| `question`    | yes      | The research question, quoted                                  |
| `status`      | yes      | `draft`, `active`, `concluded`, or `stale`                     |
| `started`     | yes      | Date research began (YYYY-MM-DD)                               |
| `concluded`   | no       | Date research concluded, `null` if open                        |
| `stale_after` | no       | Days after `concluded` before auto-marking stale (default: 90) |
| `tags`        | yes      | List of lowercase tags for cross-referencing                   |

## Research Definition of Done

A research document is **concluded** when all of the following hold:

1. **Question answered.** The Conclusions section directly addresses the
   question stated in the front matter. "We need more research" is not a
   conclusion — it's a scope expansion that needs its own research file.

2. **Scope honored.** The document covers what Scope & Constraints promised,
   nothing less. Covering more is fine if it emerged naturally.

3. **Method documented.** A skeptical reader can evaluate _how_ you reached your
   findings, not just _what_ you found. Sources are cited. Search strategy is
   explicit.

4. **Limitations stated.** At least one limitation is named. If you can't think
   of one, you haven't looked hard enough.

5. **Claims sourced.** Every factual claim either has a citation or is explicitly
   marked as inference/opinion. No unmarked speculation.

6. **Peer-reviewable.** Someone unfamiliar with the topic can follow the
   argument from Motivation through Conclusions without needing to ask you what
   you meant.

7. **Actionable.** The research connects back to a decision, design, or
   understanding. Pure knowledge accumulation without a use is a wiki article,
   not project research.

A document is **stale** when its conclusions may no longer hold due to upstream
changes (new tool versions, new documentation, shifted project goals). The
index script auto-detects staleness using the `stale_after` field. Stale
documents should be re-evaluated or archived, not silently trusted.

## Guidelines

### Formulating research questions

A good research question passes three tests:

1. **Answerable.** You can imagine what a conclusive answer looks like. "What
   are hooks?" is a topic, not a question. "Does the hooks execution model
   support parallel handlers?" has a definitive answer you could find.

2. **Scoped.** You'd know when you're done. If the question could absorb a
   month of work without a natural stopping point, it's too broad — split it.

3. **Assumption-free.** The question doesn't embed its own answer. "Why is X
   the best approach?" presupposes X wins. "What are the tradeoffs between X
   and Y?" lets the evidence lead.

Quick litmus test: can you write a Conclusions section for this question in
your head, even if you don't know the content yet? If you can picture the
shape of the answer — "it does / it doesn't," "option A wins because...,"
"it depends on these two factors" — the question is well-formed. If you can't
imagine what done looks like, tighten the question before you start.

Bad questions and their fixes:

- "How do hooks work?" → "What is the execution model for Claude Code hooks?"
- "What's the best documentation strategy?" → "What are the tradeoffs between
  curated docs-as-skills and MCP server wrappers for library documentation?"
- "Should we use focal models?" → "When do focal models outperform prompting
  Claude for classification subtasks?"

### What deserves a research file?

Not everything. Quick lookups, one-off questions answered in a conversation,
and "how do I do X" problems are not research — they're support. Research is
warranted when:

- The answer isn't obvious and requires consulting multiple sources
- The findings will inform a design decision or ADR
- You expect to reference the answer again later
- The question has enough depth that you might get it wrong on first pass

### On academic rigor

Borrow the discipline, skip the ceremony:

- **Do** state your question precisely before investigating
- **Do** document your method so findings are auditable
- **Do** distinguish evidence from inference from opinion
- **Do** name limitations honestly
- **Don't** write a standalone literature review section — weave sources into
  Findings
- **Don't** aim for false objectivity — if you're researching to make a
  decision, say so
- **Don't** over-formalize language — clear beats impressive

### On scope creep

Research expands. You start investigating hooks and end up in the execution
model of Claude Code's process isolation. When this happens:

1. Note the tangent in your current document's Limitations or Findings
2. File a new research question if it's worth pursuing
3. Do not let the current document bloat to cover both

### On AI-assisted research

When Claude (or any LLM) is a research tool:

- Treat LLM output as a **lead**, not a **source**. Follow claims back to
  primary sources before citing them.
- Document when findings came from LLM-assisted search vs. direct source review.
- Be especially skeptical of LLM-generated technical details — the
  "plausible-but-wrong" problem is real and well-documented in your own project
  history.
- Record the queries/prompts used, just as you'd record search terms.

### On the relationship to ADRs

Research informs decisions. ADRs record decisions. They are not the same
document. A research file might feed into zero, one, or many ADRs. An ADR
should reference its supporting research, not duplicate it.
