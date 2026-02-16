# Anti-Patterns in LLM Prose

Patterns that cause LLMs to interpret instructions inconsistently. Each pattern includes the problem, research basis where applicable, and fix.

---

## Highest-Impact Patterns

These patterns cause the most severe interpretation variance based on empirical research.

### Synonym Variation

Using different words for the same concept throughout a document.

**Research basis:** Word-level perturbation (synonym substitution) causes 39% average performance drop—the highest-damage perturbation type tested (PromptRobust benchmark).

| Inconsistent | Consistent |
|--------------|------------|
| "Validate input... verify the data... check parameters" | "Validate input... validate the data... validate parameters" |
| "The service handles... the system processes... the component manages" | "The service handles... the service processes... the service manages" |

**Fix:** Establish vocabulary in document preamble. Use each term in exactly one sense throughout.

```markdown
## Vocabulary

- **validate** — Check input against defined rules before processing
- **transform** — Convert data from one format to another
- **emit** — Send output to downstream consumers
```

---

### Negation as Primary Instruction

Telling the LLM what NOT to do rather than what TO do.

**Research basis:** Negation is "too small a perturbation" to reliably reverse meaning in LLM processing. Negation probing studies show LLMs struggle to properly apply semantic reversal.

| Weak (Negation) | Strong (Positive) |
|-----------------|-------------------|
| "Don't use jargon" | "Use plain language a non-specialist can understand" |
| "Never skip validation" | "Validate all inputs before processing" |
| "Don't be verbose" | "Limit responses to 2-4 sentences" |
| "Avoid making assumptions" | "State assumptions explicitly; request clarification when uncertain" |

**For genuine prohibitions, use explicit structure:**

```markdown
PROHIBITED: Committing secrets to version control
INSTEAD: Use environment variables or secret management service
```

---

### Mid-Document Critical Rules

Placing essential instructions in the middle of long documents.

**Research basis:** LLM attention is highest at document start and end, lowest in middle sections. Critical rules buried in middle get missed (OpenAI long-context research).

**Weak:**
```markdown
# Overview
[...]

# Configuration  
[...]

# Important: Never delete production data without backup
[...]

# Deployment
[...]
```

**Strong:**
```markdown
# Critical Rules
Never delete production data without backup.

# Overview
[...]

# Configuration
[...]

# Deployment
[...]

# Summary
Remember: Never delete production data without backup.
```

---

### Implicit List Exhaustiveness

Providing examples without stating whether the list is complete. See [interpretation model](interpretation-model.md#expressio-unius-expression-of-one-excludes-others) for why this matters.

**Weak:** "Supported formats: PDF, DOCX, TXT"  
**LLM interprets:** PNG is NOT supported.

**If exhaustive (intended):**  
"Supported formats (exhaustive): PDF, DOCX, TXT"

**If illustrative:**  
"Supported formats include PDF, DOCX, TXT, and other text-based formats"

---

## Standard Anti-Patterns

### Hedge Words

Words that signal uncertainty without specifying conditions.

| Avoid | Problem | Fix |
|-------|---------|-----|
| usually | When not? | State the exceptions |
| generally | What are the exceptions? | List them explicitly |
| typically | Define atypical cases | Enumerate conditions |
| often | How often? When not? | Quantify or enumerate |
| sometimes | Under what conditions? | State the conditions |
| might | What determines this? | State decision criteria |
| could consider | Should it or not? | Make recommendation explicit |

**Weak:** "Usually follow the style guide unless it doesn't make sense."  
**Strong:** "Follow the style guide. Exception: When style guide conflicts with framework requirements, framework requirements take precedence. Document deviation in PR."

---

### Implicit Conditionals

Prose that implies conditions without stating them.

**Weak:** "Senior engineers can skip code review."  
**Question:** Under what circumstances? For what changes?

**Strong:**  
```markdown
Code review skip criteria (ALL must apply):
1. Author has maintainer role
2. Change is docs-only or config-only
3. Change is <50 lines
4. No logic changes
```

**Weak:** "Use caching for performance."  
**Strong:**  
```markdown
Use caching when:
- Response time exceeds 200ms
- Data changes less than once per hour
- Cache invalidation path exists and is tested
```

---

### Undefined Qualifiers

Abstract terms that require interpretation.

| Qualifier | Problem | Fix |
|-----------|---------|-----|
| appropriate | Appropriate to whom? By what criteria? | Define criteria |
| reasonable | By what standard? | Quantify threshold |
| significant | What threshold? | State numeric or categorical threshold |
| properly | Define proper | Enumerate requirements |
| correctly | Define correct | Provide test/verification method |
| sufficient | Sufficient for what? | State minimum requirements |
| adequate | By whose measure? | Define acceptance criteria |

**Weak:** "Ensure adequate test coverage."  
**Strong:**  
```markdown
Test coverage requirements:
- Unit tests for all public methods
- Integration tests for each API endpoint
- At least 2 error paths tested per happy path
- Coverage report shows >80% line coverage
```

---

### Judgment Without Calibration

Asking for judgment without providing reference points.

**Weak:** "Use good judgment about when to ask for help."  
**Strong:**  
```markdown
Ask for help when ANY apply:
- Blocked for >30 minutes on same issue
- Solution requires changing >3 files you didn't write
- Uncertainty about correct approach after checking docs

Examples that warrant asking:
- Database schema changes
- Authentication/authorization logic
- External API integration

Examples to handle independently:
- Variable naming
- Import organization
- Formatting (covered by linter)
```

---

### Role Ambiguity

Describing responsibilities without boundaries.

**Weak:** "The architect handles design."

**Strong:**  
```markdown
## Architect Responsibilities

**Owns:**
- System boundaries and component interfaces
- Technology selection with documented rationale
- Cross-cutting concerns (auth, logging, observability)

**Does NOT own:**
- Implementation details within components (→ Engineer)
- Test strategy and coverage (→ Test Engineer)
- Deployment pipeline configuration (→ DevOps)

**Shared with Engineer:**
- API contract design (Architect leads, Engineer contributes)
- Performance optimization (Engineer proposes, Architect approves)
```

---

### Missing State Definitions

Stateful concepts without transition rules.

**Weak:** "Issues move through the workflow."

**Strong:**  
```markdown
## Issue States

[Open] → [In Progress] → [Review] → [Closed]
   ↓           ↓
[Blocked]   [Changes Requested]
              ↓
           [Review]

## Valid Transitions

| From | To | Trigger |
|------|----|---------|
| Open | In Progress | Assignee begins work |
| In Progress | Review | PR opened |
| In Progress | Blocked | External dependency identified |
| Review | Changes Requested | Reviewer requests changes |
| Changes Requested | Review | Author addresses feedback |
| Review | Closed | PR merged |
| Blocked | In Progress | Blocker resolved |
```

---

### Circular Definitions

Defining terms using themselves or equally vague synonyms.

| Circular | Non-Circular |
|----------|--------------|
| "Make appropriate decisions using good judgment" | "Decide based on: existing patterns, documented precedents, team conventions. When none apply, escalate." |
| "Handle errors properly" | "Handle errors by: logging, returning typed error, notifying if user-facing" |
| "Ensure quality is maintained" | "Quality criteria: tests pass, linter clean, review approved, no regression in metrics" |

---

### Subjective Standards

Standards that cannot be objectively verified.

**Research basis:** IFEval benchmark demonstrated verifiable instructions are followed more reliably than subjective ones.

| Subjective (Low Reliability) | Verifiable (High Reliability) |
|------------------------------|-------------------------------|
| "Be concise" | "Limit to 3-5 sentences" |
| "Write clearly" | "Use words with <3 syllables; sentences <20 words" |
| "Respond quickly" | "Respond within 200ms" |
| "Use a friendly tone" | "Use first person; acknowledge user by name if known" |
| "Don't over-explain" | "One explanation per concept; no repetition" |

---

## Recovery Pattern

When you identify an anti-pattern in your writing:

1. **Identify the ambiguity** — What word or phrase allows multiple interpretations?
2. **Classify the type** — Hedge word? Implicit conditional? Undefined qualifier? (See [ambiguity-taxonomy.md](ambiguity-taxonomy.md))
3. **Enumerate the cases** — What are all situations this could apply to?
4. **State conditions explicitly** — Under what circumstances does each case apply?
5. **Provide concrete examples** — Give instances of each case
6. **Define the boundary** — What is explicitly NOT covered?
7. **Verify objectively** — Could an LLM verify compliance? If not, add measurable criteria.
