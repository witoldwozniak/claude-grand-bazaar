# How LLMs Interpret Ambiguous Constructs

LLMs exhibit interpretation patterns that align with legal and technical conventions — likely from training data, though the exact mechanism is unverified. These patterns are *observed behaviors*, not guaranteed rules. Use them to anticipate how an LLM will probably parse ambiguous text.

## TL;DR

Three patterns cover most interpretation issues:

1. **Lists are treated as exhaustive.** Unlisted items are presumed excluded. Mark illustrative lists explicitly.
2. **Modifiers bind to nearest element.** "Valid requests and responses" → "valid" applies only to "requests."
3. **Negation is unreliable.** "Don't do X" is weaker than "Do Y instead."

## Patterns That Align With Legal Canons

### Expressio Unius (Expression of One Excludes Others)

When you list specific items, unlisted items are presumed excluded.

**Write:** "Supported formats: PDF, DOCX, TXT"  
**LLM interprets:** PNG is NOT supported (unlisted = excluded)

**If you mean non-exhaustive:**  
"Supported formats include PDF, DOCX, TXT, and other text-based formats"  
Or: "Supported formats (non-exhaustive): PDF, DOCX, TXT"

**Application:** Always mark lists as exhaustive or illustrative. Default assumption: exhaustive.

---

### Last Antecedent Rule

A qualifying phrase applies only to the immediately preceding element.

**Write:** "Validate user input and API responses from external services"  
**LLM interprets:** "from external services" modifies only "API responses," not "user input"

**If you mean both:**  
"Validate user input from external services and API responses from external services"  
Or: "Validate both user input and API responses when they originate from external services"

**Application:** Place modifiers immediately after what they modify. When in doubt, restructure to eliminate ambiguity.

---

### Ejusdem Generis (Of the Same Kind)

General terms following specific items inherit the category of those items.

**Write:** "Block requests from bots, scrapers, and similar sources"  
**LLM interprets:** "similar sources" means automated/non-human sources (same category as bots, scrapers)

**Write:** "Reject invalid input: null, empty string, and other bad values"  
**LLM interprets:** "other bad values" means validation failures (null, empty belong to this category)

**Application:** When using catchall phrases, ensure examples clearly establish the intended category.

---

## Structural Parsing Patterns

### Format Is Semantic

Research shows semantically equivalent prompts with different formats cause up to 76 percentage points of accuracy variance (Sclar et al., ICLR 2024). Format affects parsing, not just readability.

**High-reliability structures:**
- Numbered lists for sequences
- Bullet points for unordered sets  
- Tables for relationships
- Headers for section boundaries
- Consistent delimiters (XML tags, markdown)

**Low-reliability structures:**
- Dense prose paragraphs with embedded logic
- Comma-separated inline lists for complex items
- Implicit hierarchy through indentation alone

---

### Attention Distribution

LLM attention is highest at document start and end, lowest in middle sections.

**Implication for long documents:**
- Place critical instructions at beginning
- Repeat critical instructions at end
- Don't bury essential rules in middle sections

**Document bookending pattern:**
```markdown
# Instructions

[Critical rule stated first]

[Body content...]

# Summary

[Critical rule restated]
```

---

### Modifier Binding

LLMs apply proximity heuristics for modifier attachment.

**Write:** "Process valid requests and responses"  
**Ambiguous:** Does "valid" apply to both, or only "requests"?

**Patterns by modifier position:**

| Construction | Likely Interpretation |
|--------------|----------------------|
| "Valid requests and responses" | "Valid" → requests only |
| "Valid requests and valid responses" | "Valid" → both (explicit) |
| "Requests and responses that are valid" | "Valid" → both (postmodifier) |

**Application:** For critical modifiers, either repeat for each element or use postmodifier position.

---

## Quantifier Scope

### Default Quantifier Binding

**Write:** "Every user can access some resources"  
**Ambiguous:** Same resources for all users, or different resources per user?

**Clearer constructions:**
- "Every user can access the shared resource pool" (same for all)
- "Each user can access their assigned resources" (different per user)

### Implicit Universal vs. Existential

**Write:** "Errors should be logged"  
**Ambiguous:** All errors? Some errors? Which errors?

**State scope explicitly:**
- "Log all errors" (universal)
- "Log errors that affect user experience" (conditional)
- "Log at least one error per failed operation" (existential minimum)

---

## Negation Processing

LLMs process negation unreliably. "Not" is often too weak a signal to reverse meaning.

### Negation Reliability Hierarchy

| Construction | Reliability | Example |
|--------------|-------------|---------|
| Positive instruction | Highest | "Use formal tone" |
| Explicit prohibition structure | Medium | "PROHIBITED: informal tone" |
| Inline negation | Low | "Don't use informal tone" |
| Negative prefix | Lowest | "Use non-informal tone" |

### Reframe Negations

**Instead of:** "Don't include personal opinions"  
**Write:** "State facts and evidence only"

**Instead of:** "Never skip validation"  
**Write:** "Validate all inputs before processing"

**When prohibition is essential:**
```markdown
PROHIBITED: Committing secrets to repository
INSTEAD: Use environment variables or secret management service
```

---

## Pronoun Resolution

LLMs resolve pronouns using recency and salience heuristics, which can fail.

**Write:** "The parser processes the input. It validates syntax."  
**Ambiguous:** Does "it" refer to parser or input?

**Resolution patterns:**

| Ambiguous | Clear |
|-----------|-------|
| "The service calls the API. It retries on failure." | "The service calls the API. The service retries on failure." |
| "If the request fails, handle it appropriately." | "If the request fails, log the failure and return error response." |

**Application:** Repeat nouns rather than use pronouns, especially across sentence boundaries.

---

## Conditional Parsing

### If-Then Completeness

LLMs expect conditionals to specify both branches.

**Write:** "If the user is authenticated, show the dashboard."  
**LLM may assume:** If NOT authenticated, do nothing (implicit else)

**Complete conditional:**
```markdown
IF user is authenticated:
  Show dashboard
ELSE:
  Redirect to login page
```

### Nested Conditional Clarity

**Ambiguous:** "If A and B or C, then D"  
**Could mean:** (A AND B) OR C → D, or A AND (B OR C) → D

**Use explicit grouping:**
```markdown
Condition: (A AND B) OR C
Action: D
```

Or enumerate:
```markdown
Execute D when ANY of:
1. Both A and B are true
2. C is true
```

---

## Sources

- Sclar et al. (2024). "Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design" — ICLR 2024. Format variance findings.
- Zhu et al. (2023). "PromptRobust: Towards Evaluating the Robustness of Large Language Models on Adversarial Prompts" — Synonym substitution impact.
- Zhou et al. (2023). "Instruction-Following Evaluation for Large Language Models" (IFEval) — Verifiable vs. subjective instruction compliance.
- Legal interpretation patterns derived from standard canons of construction (expressio unius, ejusdem generis, last antecedent rule).
