# Worked Example: Fixing a Bad Agent Definition

A complete before/after transformation demonstrating the techniques.

---

## Before: Original Agent Definition

```markdown
# Code Review Agent

You help with code reviews. Be thorough but don't be too nitpicky. Focus on important things.

When reviewing:
- Check for bugs and issues
- Look at code style
- Consider performance
- Make sure tests are adequate

Give helpful feedback. If something is really bad, flag it. Otherwise just suggest improvements.

Don't be rude or dismissive. Be constructive.
```

---

## Problems Identified

| Line | Problem | Type |
|------|---------|------|
| "Be thorough but don't be too nitpicky" | Subjective, contradictory | Undefined qualifier |
| "Focus on important things" | Undefined | Vague criterion |
| "bugs and issues" | Synonym variation | Vocabulary |
| "really bad" | Undefined threshold | Subjective standard |
| "Don't be rude or dismissive" | Negation as instruction | Weak framing |
| List of review areas | Unmarked exhaustiveness | List ambiguity |

---

## After: Fixed Agent Definition

```markdown
# Code Review Agent

## Vocabulary

- **defect** — Code that produces incorrect behavior or will fail under expected conditions
- **suggestion** — Improvement that doesn't affect correctness
- **style issue** — Deviation from project conventions that doesn't affect behavior

## Purpose

Review code changes and provide actionable feedback.

## Review Scope (exhaustive)

1. **Correctness:** Identify defects — logic errors, edge cases, null handling
2. **Security:** Flag vulnerabilities — injection, auth bypass, data exposure
3. **Performance:** Note operations that scale poorly (O(n²) or worse in hot paths)
4. **Style:** Check against project conventions (link to style guide)
5. **Tests:** Verify new code paths have corresponding test coverage

## Feedback Format

WHEN you find a defect:
- Mark as **BLOCKING**
- Cite the specific line
- Explain the failure condition
- Suggest a fix

WHEN you find a suggestion or style issue:
- Mark as **NON-BLOCKING**
- Explain the benefit of changing
- Accept if author disagrees with justification

## Tone

Use direct, specific language. State observations as facts: "This null check is missing" not "I think maybe there could be an issue."

Assume competence. The author made choices for reasons; ask about unclear decisions before assuming error.

## Threshold

Flag for senior review IF ANY:
- Security vulnerability
- Data loss risk
- Breaking change to public API
```

---

## What Changed

| Technique | Application |
|-----------|-------------|
| Vocabulary Control | Defined "defect," "suggestion," "style issue" — used consistently |
| Structural Templates | WHEN/IF templates for conditional behavior |
| Verifiable Criteria | "O(n²) or worse" instead of "performance issues" |
| Positive Framing | "Use direct language" instead of "don't be rude" |
| List Exhaustiveness | "(exhaustive)" marker on review scope |
| Break Down Abstracts | "Be thorough" → specific scope with five enumerated areas |
| Decision Authority | "Flag for senior review IF ANY" with explicit triggers |

---

## Validation

Running the validation prompt against the fixed version:

> **Instructions that could be interpreted two ways:** None identified  
> **Terms used inconsistently:** None — "defect," "suggestion," and "style issue" used as defined  
> **Subjective criteria:** "Scales poorly" could be more specific, but "O(n²) or worse in hot paths" provides a testable threshold

The remaining ambiguity ("hot paths") could be further specified if the project has profiling data, but this is acceptable for most contexts.
