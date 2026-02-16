---
name: write-for-llms
description: Write precise, unambiguous prose optimized for LLM consumption. Use when creating agent definitions, system prompts, skills, commands, specs, procedures, or any document that LLMs will read and act on repeatedly. Trigger phrases include "optimize this prompt", "review system prompt", "make this clearer for LLMs", "ambiguous instruction". Focuses on durable artifacts where consistent interpretation matters.
author: witoldwozniak
license: Hippocratic-3.0
---

# LLM Prose

Goal: documents with single valid interpretation.

## Foundation (apply first — these fix the most common errors)

### Vocabulary Control

Use one term per concept throughout. Synonym variation causes 39% average performance degradation (Zhu et al., "PromptRobust," 2023).

Define terms in a glossary, then use them exactly. "Validate input" — not "check input" or "verify input."

### Structural Templates

Format affects interpretation as much as content. Use templates for conditionals (exhaustive):

| Pattern | Template |
|---------|----------|
| Always | "The system shall [action]" |
| Triggered | "WHEN [event], the system shall [action]" |
| Stateful | "WHILE [condition], the system shall [action]" |
| Branching | "IF [condition], THEN [action], ELSE [alternative]" |

**Before:** "Senior engineers can skip review."  
**After:** "IF author has maintainer role AND change is <50 lines AND change is docs-only, THEN review is optional."

---

## Precision

### Verifiable Criteria

Replace subjective standards with testable conditions.

| Subjective | Verifiable |
|------------|------------|
| "Be concise" | "Limit to 3-5 sentences" |
| "Respond quickly" | "Respond within 200ms" |
| "Appropriate detail" | "One paragraph for simple queries; up to three for complex" |

**Test:** Could an LLM verify compliance? IF not verifiable, THEN add measurable criteria.

### Positive Framing

Frame instructions positively. Negation is unreliable — LLMs struggle to reverse meaning.

| Weak | Strong |
|------|--------|
| "Don't use jargon" | "Use plain language" |
| "Never skip validation" | "Validate all inputs" |
| "Avoid assumptions" | "State assumptions explicitly" |

For genuine prohibitions: "PROHIBITED: [action]. INSTEAD: [alternative]."

---

## Architecture (long documents)

- **Bookending:** Place critical rules at beginning AND end (attention lowest in middle)
- **Constraints:** Separate hard constraints from adjustable defaults
- **Authority:** For multi-role systems, define who decides what and escalation triggers
- **Output anchoring:** End prompts with the beginning of the desired output structure — dramatically improves format compliance by priming the model's continuation

---

## Disambiguation

### Break Down Abstracts

Abstract concepts need enumerated subtypes AND boundary examples.

**Before:** "Be honest."  
**After:** "Truthful (assert only believed true), Calibrated (acknowledge uncertainty), Non-deceptive (no false impressions)."

**Before:** "Avoid over-engineering."  
**After:** "Acceptable complexity: abstraction with 2+ implementations, documented extensibility requirement. Simpler otherwise."

### Handling Residual Ambiguity

**Population heuristic:** When a request can't be fully disambiguated, imagine 1000 different users sending the exact same message. What distribution of intents would exist? Design for the most common intent; document handling for others.

*Example:* User says "make it shorter." 1000 users sending this probably mean: 60% reduce word count, 25% simplify language, 10% remove sections, 5% something else. Design for "reduce word count" as default, but document: "If you meant simplify language or remove sections, say so."

**State transitions:** For stateful concepts, define valid states and transition conditions.

**When disambiguation fails:** IF irreducible ambiguity remains, THEN make the document acknowledge it explicitly: "This instruction is intentionally flexible. Interpret based on [criteria]." or "When uncertain between X and Y, prefer X."

### List Exhaustiveness

LLMs assume lists are exhaustive. Mark illustrative lists: "Supported formats include X, Y, and similar" vs. "Supported: X, Y" (exhaustive).

### Modifier Binding

Modifiers attach to the nearest element. "Valid requests and responses" → "valid" applies only to "requests."

Place modifiers immediately after what they modify. WHEN writing complex multi-clause sentences, read [interpretation-model.md](references/interpretation-model.md) for additional patterns.

---

## Verification

### Self-Audit Checklist (exhaustive)

- [ ] Each term used in one sense throughout?
- [ ] Conditionals use WHEN/IF/WHILE templates?
- [ ] Standards are verifiable, not subjective?
- [ ] Instructions framed positively?
- [ ] For long documents: critical rules at start and end?
- [ ] Abstract concepts broken into subtypes with boundary examples?
- [ ] Lists marked exhaustive or illustrative?
- [ ] Every pronoun has unambiguous referent?
- [ ] Modifiers placed immediately after what they modify?

### Triage Priority

WHEN multiple issues exist, fix in this order:
1. Vocabulary inconsistency (foundations; other fixes may fail)
2. Missing WHEN/IF/WHILE templates (structure before content)
3. Subjective standards (testability)
4. List exhaustiveness markers (interpretation)
5. Modifier binding (refinement)

### Chain-of-Verification (CoVe)

After generating output, ask the model to verify its own response against the source document. Research shows CoVe improves accuracy by up to 23%. Add to verification workflows: "After generating your answer, verify that all claims are supported by the provided context."

### Interpretation Test

After writing, verify: "Could a different LLM instance read this and produce the same interpretation?"

**Validation prompt:** Give your document to another LLM with this prompt:
```
Read this document and list:
1. Any instructions that could be interpreted two different ways
2. Any terms used inconsistently  
3. Any criteria that are subjective (you couldn't verify compliance programmatically)
```

IF uncertain about specific passages, THEN apply the [ambiguity taxonomy](references/ambiguity-taxonomy.md).

---

## Anti-Patterns

WHEN encountering repeated interpretation failures, read [anti-patterns.md](references/anti-patterns.md) for detailed patterns and fixes.

**Highest impact (illustrative):**
- Synonym variation — 39% performance degradation (worst single perturbation)
- Negation as primary instruction — LLMs fail to reverse meaning reliably
- Mid-document critical rules — lowest attention zone; rules get missed
- Implicit list exhaustiveness — LLMs assume unlisted items excluded
- Hedge words ("usually", "generally") — create unspecified exception cases
- Undefined qualifiers ("appropriate", "adequate") — untestable standards

### Reference Loading

| Reference | Load when |
|-----------|-----------|
| [interpretation-model.md](references/interpretation-model.md) | Complex multi-clause sentences or modifier binding issues |
| [ambiguity-taxonomy.md](references/ambiguity-taxonomy.md) | Self-audit reveals uncertain passages |
| [anti-patterns.md](references/anti-patterns.md) | Repeated interpretation failures |
| [worked-example.md](references/worked-example.md) | Need full before/after transformation |
| [prompt-techniques.md](references/prompt-techniques.md) | Token efficiency, output anchoring examples, meta-prompting, extended thinking |

**Do NOT load all references** for simple prompt reviews. This document contains sufficient guidance for most tasks.

---

## Scope

**Use for (illustrative):** Agent definitions, system prompts, skills, commands, procedures, specs — any document an LLM will interpret repeatedly
**Not for:** One-off queries, user-facing documentation, creative content, conversation

**Related techniques:** Extended thinking triggers ("think" → "think hard" → "ultrathink") for deeper reasoning on complex prompts. Meta-prompting — using an LLM to critique and improve prompts. See [prompt-techniques.md](references/prompt-techniques.md) for detailed patterns.

---

## Limitations

**Relax when:** Mixed LLM + human audience, creative content, exploratory drafts, teaching materials.  
**Apply strictly when:** System prompts, agent definitions, executable specs, any document where "LLM did something unexpected" is a failure mode.

---

## Core Rules (bookend)

- Use one term per concept throughout
- IF/WHEN/WHILE templates for all conditionals
- Verifiable criteria over subjective standards
- PROHIBITED: [action]. INSTEAD: [alternative] for prohibitions

**Goal:** Single valid interpretation. Every technique serves this.
