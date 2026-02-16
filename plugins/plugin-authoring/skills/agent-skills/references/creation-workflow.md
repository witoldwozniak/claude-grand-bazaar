# Workflow: Create or Update a Skill

Follow these steps in order, skipping only when clearly not applicable.

## Step 1: Understand with Concrete Examples

Skip only when usage patterns are already clearly understood.

Understand concrete examples of how the skill will be used. Ask targeted questions:

- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would a user say that should trigger this skill?"

Avoid overwhelming the user — start with the most important questions, follow up as needed. Conclude when the functionality scope is clear.

## Step 2: Plan Reusable Contents

Analyze each concrete example to identify reusable resources:

1. Consider how to execute the example from scratch
2. Identify what scripts, references, and assets would help when executing repeatedly

| Example task | Reusable resource |
|---|---|
| "Rotate this PDF" → same code each time | `scripts/rotate_pdf.py` |
| "Build me a todo app" → same boilerplate | `assets/hello-world/` template |
| "How many users logged in?" → rediscover schemas | `references/schema.md` |

## Step 3: Initialize the Skill

Skip if the skill already exists. When creating from scratch, run the init script:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates the skill directory with a SKILL.md template and example `scripts/`, `references/`, `assets/` directories. Customize or remove generated files as needed.

## Step 4: Edit the Skill

The skill is for another instance of Claude. Include information that is beneficial and non-obvious. Consider what procedural knowledge, domain-specific details, or reusable assets would help another Claude instance execute effectively.

### Implement Reusable Contents First

Start with the resources identified in Step 2. This may require user input (e.g., brand assets, documentation).

Test added scripts by running them. For many similar scripts, test a representative sample.

Delete example files from initialization that aren't needed.

### Consult Design Pattern Guides

- **Multi-step processes**: See `references/workflows.md` for sequential and conditional workflow patterns
- **Output format standards**: See `references/output-patterns.md` for template and example patterns

### Write SKILL.md

**Frontmatter**: Write `name` and `description` following the Skill Structure guidelines in SKILL.md. Add optional fields (`author`, `license`, etc.) as needed.

**Body**: Write instructions in imperative/infinitive form. See Writing Style in SKILL.md.

## Step 5: Package the Skill

Package into a distributable `.skill` file:

```bash
scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

The script validates automatically (frontmatter, naming, description, structure) then packages if validation passes. Fix any errors and re-run.

For quick validation during development:

```bash
scripts/quick_validate.py <path/to/skill-folder>
```

## Step 6: Test the Skill (TDD)

**Core principle:** If an agent wasn't observed failing without the skill, the skill's value is unproven.

| Phase | Action |
|-------|--------|
| **RED** | Run pressure scenarios WITHOUT skill, document failures |
| **GREEN** | Write skill addressing those specific failures |
| **REFACTOR** | Find new rationalizations, add explicit counters, re-test |

For discipline-enforcing skills, use **pressure scenarios** combining 3+ pressures (time, sunk cost, authority, exhaustion). See `references/persuasion-principles.md` for research on how persuasion psychology informs skill design under pressure.

See `references/testing-skills-with-subagents.md` for complete testing methodology.

## Step 7: Iterate

After real usage, improve the skill:

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or resources should change
4. Implement changes, re-test
