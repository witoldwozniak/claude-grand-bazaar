# Example Evaluation

Target: A hypothetical `discuss` skill (~45 lines)

## Specification Checks

- [x] Folder name is kebab-case
- [x] File is exactly SKILL.md
- [x] No README.md inside
- [x] Valid YAML frontmatter
- [x] Name ≤64 chars, valid format
- [x] Description ≤1024 chars, no XML
- [x] Under ~500 lines (narrow skill)
- [x] WHAT stated: "Pick a note for casual discussion"
- [x] WHEN stated: "Use when user runs /discuss, asks to discuss a note"
- [x] Keywords present: "discuss", "chat about notes", "serendipitous"

## Observations

**Description Quality:** Strong trigger coverage. "Discuss a note", "chat about notes", and "/discuss" all included. Risk of false positive on generic "discuss" without vault context.

**Knowledge Value:** Selection criteria (prefer substantive, thought-provoking, connected notes) provide value Claude wouldn't infer. Exclusion list (templates/, archive/, daily notes) prevents obvious mistakes. Conversation style section mostly restates Claude's defaults.

**Progressive Disclosure:** 45 lines is appropriately minimal. No references needed.

**Freedom Calibration:** High freedom matches the creative/exploratory nature of the task. No fragile operations.

**Practical Completeness:** Example openers show expected output format. No decision trees needed for this simple workflow.

## Recommendations

1. **Delete "Conversation Style" section** — Claude defaults to casual, question-asking behavior. Four lines that add no value.
2. **Add negative trigger in description** — "Not for structured note review or editing" to prevent false positives.
3. **Consider adding fallback** — What if vault has <5 substantive notes?
