# Skill Specification Checklist

Use this checklist when creating or evaluating a skill. Every item is binary pass/fail.

## Structure

- [ ] Folder name is kebab-case
- [ ] File is exactly `SKILL.md` (case-sensitive)
- [ ] No README.md or extraneous files (CHANGELOG.md, INSTALLATION_GUIDE.md, etc.)
- [ ] YAML frontmatter with opening and closing `---`
- [ ] Required fields present: `name`, `description`
- [ ] All referenced files exist (`scripts/`, `references/`, `assets/`)
- [ ] If `context: fork` is set, `agent` field is also present
- [ ] `allowed-tools` values are valid tool names (if present)
- [ ] `hooks` structure matches hook schema (if present)
- [ ] `model` value is valid: `sonnet` / `opus` / `haiku` / `inherit` (if present)
- [ ] Variable substitutions (`$ARGUMENTS`, `${CLAUDE_SESSION_ID}`) tested and working

## Naming

- [ ] `name` field: ≤64 chars, lowercase alphanumeric + hyphens only
- [ ] No `--`, doesn't start/end with `-`
- [ ] `name` matches folder name

## Description

- [ ] ≤1024 chars, no XML tags
- [ ] Written in third person
- [ ] States WHAT (specific capability)
- [ ] States WHEN (trigger scenarios with "Use when...")
- [ ] Includes keywords matching natural user phrasings
- [ ] No false-positive triggers (too broad)
- [ ] No missing triggers (too narrow)

## Content

- [ ] Instructions in imperative/infinitive form (not second person)
- [ ] Narrow skills: SKILL.md under ~500 lines
- [ ] Meta-skills: additional length is routing infrastructure only (decision trees, reference overviews)
- [ ] SKILL.md body under 5000 words
- [ ] Content that could move to references without hurting routing has been moved
- [ ] References explicitly mentioned in SKILL.md with when-to-read guidance
- [ ] Progressive disclosure used appropriately (metadata → SKILL.md → references)
- [ ] No deeply nested references (all one level from SKILL.md)
- [ ] Reference files >100 lines include a table of contents

## Testing

- [ ] Skill triggers for intended use cases
- [ ] Skill content helps execute tasks
- [ ] Scripts (if any) tested and working
- [ ] References (if any) accessible and properly formatted
