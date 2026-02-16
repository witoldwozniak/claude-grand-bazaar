# Prompt Techniques

Supplementary patterns for optimizing LLM-targeted prose beyond the core SKILL.md guidance.

## Extended Thinking Triggers

Specific phrases map to increasing computation budgets in Claude:

| Trigger | Budget | Use When |
|---------|--------|----------|
| "think" | Basic extended thinking | Standard multi-step reasoning |
| "think hard" | Increased computation | Complex architectural decisions |
| "ultrathink" | Maximum reasoning budget | Subtle bugs, deep analysis across large codebases |

Reserve higher budgets for tasks where the token investment delivers proportional value. For routine tasks, basic "think" or no trigger is sufficient.

## CO-STAR Framework

Systematic structure for complex prompts — ensures no critical element is overlooked:

| Element | Purpose | Example |
|---------|---------|---------|
| **C**ontext | Background information | "This is a TypeScript monorepo with 50k LOC" |
| **O**bjective | What to achieve | "Refactor the auth module to use JWT" |
| **S**tyle | Writing/code style | "Match existing patterns in src/modules/" |
| **T**one | Emotional quality | "Direct, technical, no hedging" |
| **A**udience | Who consumes output | "Senior developers reviewing the PR" |
| **R**esponse | Format specification | "Return a numbered list of changes with file paths" |

Not every prompt needs all six elements. Apply when prompt complexity warrants it.

## Output Anchoring

End prompts with the beginning of the desired output structure. This primes the model's continuation and dramatically improves format compliance.

**Without anchoring:**
```
Analyze this code for security issues.
```

**With anchoring:**
```
Analyze this code for security issues. Start your response with:
- Vulnerability Type:
- Severity:
- Location:
- Recommended Fix:
```

Anchoring works because LLMs predict continuations based on patterns. Providing the output start constrains the continuation space to the desired format.

## Meta-Prompting

Use an LLM to improve prompts — particularly effective for CLAUDE.md files and system prompts:

1. Write initial prompt
2. Ask Claude: "Critique this prompt. Identify ambiguities, missing context, and potential misinterpretations."
3. Revise based on feedback
4. Repeat until stable

Anthropic recommends running CLAUDE.md files through this process periodically as projects evolve.

## Token Efficiency

### Directive Prose

System prompts and agent definitions accumulate hedging and filler. Stripping these yields ~30-40% token savings with no loss of clarity:

| Verbose (system prompt) | Efficient |
|-------------------------|-----------|
| "You should always make sure to validate all user inputs before processing them" | "Validate all user inputs before processing" |
| "It is important that the response format matches the specification provided below" | "Match response format to the specification below" |
| "Please ensure that you do not include any sensitive information in your responses" | "PROHIBITED: sensitive information in responses" |

Common multi-word fillers that appear in LLM-targeted documents:

| Filler | Replace with |
|--------|-------------|
| "in order to" | "to" |
| "due to the fact that" | "because" |
| "make sure to" | (remove — use imperative directly) |
| "it is important that" | (remove — state the rule directly) |

### Prompt Caching Placement

Both Anthropic and OpenAI cache repeated prompt prefixes — cached tokens cost ~10% of normal. Structure prompts to place static content (system instructions, examples, reference material) early, with variable content at the end.

### Minimum Viable Prompt

Start with essential information only. Expand only when simpler prompts produce incorrect output.

- "Python: binary search function" may be sufficient
- Expand to "Python: binary search function for sorted integer list, return index or -1" only if the minimal prompt produces incorrect output

The efficiency-effectiveness tradeoff resolves better than expected: concise, well-structured prompts often outperform verbose ones on both cost and accuracy.
