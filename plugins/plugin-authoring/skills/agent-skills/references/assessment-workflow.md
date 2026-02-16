# Workflow: Assess a Skill

Evaluate skills by producing structured observations, not scores. Grades create false precision — observations surface real issues.

## Output Structure

Every evaluation produces three sections:

```markdown
## Specification Checks
[Binary pass/fail against spec]

## Observations
[Structured notes on content quality]

## Recommendations
[Prioritized, actionable improvements]
```

## Phase 1: Specification Checks

Run the binary pass/fail checklist in `references/spec-checklist.md` against the target skill. Report all failures.

## Phase 2: Observations

For each area, write 1-3 sentences about what you observe. No scoring.

**Description Quality** — Does the description enable correct triggering? Are there false-positive triggers (too broad)? Missing triggers (too narrow)?

**Knowledge Value** — What does this skill teach that Claude doesn't already know? Does it reference specific tools, APIs, versions, edge cases, failure modes? For each paragraph, ask: *"If Claude had only the task description, would it produce equivalent guidance?"* YES → wastes tokens. NO → adds value.

**Progressive Disclosure** — Is context loaded efficiently? Is core guidance in SKILL.md with details in references/? Could the skill be shorter without losing value?

**Freedom Calibration** — Do constraints match task fragility? Evaluate against the Degrees of Freedom framework in SKILL.md's Core Principles.

**Practical Completeness** — Can Claude actually follow this? Are there decision points without guidance, referenced tools that don't exist, missing input/output examples, or absent error recovery paths?

## Phase 3: Recommendations

Produce 3-5 prioritized improvements:

```markdown
1. **[Action verb] [specific change]** — [why it matters]
2. ...
```

Priority order:
1. Specification violations (Phase 1 failures)
2. Triggering problems (skill won't load when needed)
3. Knowledge value issues (skill wastes tokens on known content)
4. Structural improvements (progressive disclosure, freedom calibration)

See `references/evaluation-example.md` for a complete example evaluation.
