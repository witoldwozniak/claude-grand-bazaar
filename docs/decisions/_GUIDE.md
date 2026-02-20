---
title: Decision Records
description: "How and when to write Architecture Decision Records using the MADR format."
---

# Decision Records

We use the MADR format and call these "ADRs" by convention, but not every decision worth recording is strictly architectural. Project governance, versioning strategy, and workflow conventions belong to this category too. The folder is `docs/decisions/` — if it's a decision that matters to someone arriving later, it goes there.

## Format

[MADR](https://adr.github.io/madr/) with YAML front matter. Template at `docs/decisions/_TEMPLATE.md`.

### Front matter fields

| Field             | Required | Description                                                              |
| ----------------- | -------- | ------------------------------------------------------------------------ |
| `title`           | yes      | Short decision title                                                     |
| `status`          | yes      | `draft`, `proposed`, `accepted`, `superseded`, or `deprecated`           |
| `date`            | yes      | Date decision was made (YYYY-MM-DD)                                      |
| `decision-makers` | yes      | List of GitHub/git usernames who made or approved the decision           |

## Location

`docs/decisions/`

## Naming

`NNNN-descriptive-title.md` — four-digit sequential number, lowercase with hyphens. No "adr" prefix; the directory makes the purpose clear.

## Statuses

- **Draft** — leaning toward this decision, not yet committed.
- **Proposed** — formally proposed, open for discussion.
- **Accepted** — decision is in effect.
- **Deprecated** — no longer relevant.
- **Superseded** — replaced by a later ADR (link to successor).

## Decision-Makers

The `decision-makers` field in the frontmatter identifies who made or approved the decision. Use a GitHub username, git username, or e-mail — something that resolves to a real person in the project's history.

## What Warrants an ADR

Decisions where the alternatives were real contenders and the reasoning for the choice matters to someone arriving later. Not every convention needs one — if the doctrine or a strategy doc captures it well enough, that's sufficient.

When in doubt, write one. A short ADR that turns out unnecessary is cheaper than a missing one that forces someone to reverse-engineer your reasoning.

## Workflow

Discuss wherever — Claude conversations, GitHub Issues, pull requests, a napkin. When a decision crystallizes, record it as a markdown file in `docs/decisions/`. Link relevant sources in the ADR's "More Information" section.

Discussion can happen anywhere. Decisions live in the repository.

## Backfilling

Past decisions that shaped the Bazaar's architecture may be recorded retroactively. These carry the date the decision was effectively made, not the date the ADR was written.
