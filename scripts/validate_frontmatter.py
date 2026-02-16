#!/usr/bin/env python3
"""Validate YAML front matter across all document types.

Document types and their rules:
- ADRs (docs/decisions/NNNN-*.md): title, status, date, decision-makers required;
  status in {draft, proposed, accepted, superseded, deprecated}; date is YYYY-MM-DD
- Research (docs/research/*.md): question, status, started, tags required;
  status in {draft, active, concluded, stale}; started is YYYY-MM-DD
- Skills (plugins/*/skills/*/SKILL.md): name, description required; name is kebab-case
- Agents (plugins/*/agents/*.md): name, description required;
  model (if present) in {sonnet, opus, haiku, inherit}

Exit 0 if all checks pass, exit 1 if any fail.
"""

import re
import sys
from datetime import date as date_type
from pathlib import Path

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
ADR_NUMBER_RE = re.compile(r"^\d{4}-")
KEBAB_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")

ADR_STATUSES = {"draft", "proposed", "accepted", "superseded", "deprecated"}
RESEARCH_STATUSES = {"draft", "active", "concluded", "stale"}
AGENT_MODELS = {"sonnet", "opus", "haiku", "inherit"}

DECISIONS_DIR = Path("docs/decisions")
RESEARCH_DIR = Path("docs/research")
PLUGINS_DIR = Path("plugins")


def parse_front_matter(text: str) -> dict | None:
    """Extract front matter fields without a YAML dependency.

    Handles inline lists [a, b], block lists (- item), multiline values (|).
    """
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None

    fields: dict = {}
    current_key: str | None = None
    current_list: list | None = None
    multiline_value: list[str] | None = None

    for line in match.group(1).splitlines():
        stripped = line.strip()

        # Accumulate multiline scalar (|)
        if multiline_value is not None:
            if line.startswith("  ") or line.startswith("\t"):
                multiline_value.append(line.strip())
                fields[current_key] = "\n".join(multiline_value)
                continue
            else:
                multiline_value = None

        if not stripped or stripped.startswith("#"):
            continue

        # Block list item: "  - value"
        if line.startswith("  - ") and current_key is not None:
            if current_list is None:
                current_list = []
            current_list.append(line.strip()[2:].strip())
            fields[current_key] = current_list
            continue

        # Flush any pending list
        current_list = None

        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        current_key = key

        # Multiline scalar indicator
        if value == "|":
            multiline_value = []
            fields[key] = ""
            continue

        # Inline list: [a, b, c]
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
        # Quoted string
        elif value.startswith(("'", '"')) and value.endswith(("'", '"')):
            value = value[1:-1]
        # Null
        elif value == "null":
            value = None
        # Empty value (block list follows)
        elif value == "":
            current_list = []
            value = current_list

        fields[key] = value

    return fields


def validate_adr(path: Path, fields: dict) -> list[str]:
    """Validate an ADR's front matter."""
    errors = []
    for req in ("title", "status", "date", "decision-makers"):
        if not fields.get(req):
            errors.append(f"{path}: missing required field '{req}'")

    status = fields.get("status")
    if status and status not in ADR_STATUSES:
        errors.append(
            f"{path}: invalid status '{status}' "
            f"(expected one of: {', '.join(sorted(ADR_STATUSES))})"
        )

    date_val = fields.get("date")
    if date_val:
        try:
            date_type.fromisoformat(str(date_val))
        except ValueError:
            errors.append(f"{path}: invalid date '{date_val}' (expected YYYY-MM-DD)")

    return errors


def validate_research(path: Path, fields: dict) -> list[str]:
    """Validate a research document's front matter."""
    errors = []
    for req in ("question", "status", "started", "tags"):
        if not fields.get(req):
            errors.append(f"{path}: missing required field '{req}'")

    status = fields.get("status")
    if status and status not in RESEARCH_STATUSES:
        errors.append(
            f"{path}: invalid status '{status}' "
            f"(expected one of: {', '.join(sorted(RESEARCH_STATUSES))})"
        )

    started = fields.get("started")
    if started:
        try:
            date_type.fromisoformat(str(started))
        except ValueError:
            errors.append(f"{path}: invalid started date '{started}' (expected YYYY-MM-DD)")

    return errors


def validate_skill(path: Path, fields: dict) -> list[str]:
    """Validate a skill's front matter."""
    errors = []
    for req in ("name", "description"):
        if not fields.get(req):
            errors.append(f"{path}: missing required field '{req}'")

    name = fields.get("name")
    if name and not KEBAB_RE.match(str(name)):
        errors.append(f"{path}: name '{name}' is not kebab-case")

    return errors


def validate_agent(path: Path, fields: dict) -> list[str]:
    """Validate an agent's front matter."""
    errors = []
    for req in ("name", "description"):
        if not fields.get(req):
            errors.append(f"{path}: missing required field '{req}'")

    model = fields.get("model")
    if model and model not in AGENT_MODELS:
        errors.append(
            f"{path}: invalid model '{model}' "
            f"(expected one of: {', '.join(sorted(AGENT_MODELS))})"
        )

    return errors


def collect_and_validate() -> list[str]:
    """Find all documents and validate their front matter."""
    all_errors: list[str] = []
    counts = {"adrs": 0, "research": 0, "skills": 0, "agents": 0}

    # ADRs
    if DECISIONS_DIR.is_dir():
        for path in sorted(DECISIONS_DIR.glob("*.md")):
            if not ADR_NUMBER_RE.match(path.name):
                continue
            text = path.read_text(encoding="utf-8")
            fields = parse_front_matter(text)
            if fields is None:
                all_errors.append(f"{path}: no front matter found")
                continue
            counts["adrs"] += 1
            all_errors.extend(validate_adr(path, fields))

    # Research
    if RESEARCH_DIR.is_dir():
        for path in sorted(RESEARCH_DIR.glob("*.md")):
            if path.name.startswith("_"):
                continue
            text = path.read_text(encoding="utf-8")
            fields = parse_front_matter(text)
            if fields is None:
                all_errors.append(f"{path}: no front matter found")
                continue
            counts["research"] += 1
            all_errors.extend(validate_research(path, fields))

    # Skills and Agents
    if PLUGINS_DIR.is_dir():
        for skill_path in sorted(PLUGINS_DIR.glob("*/skills/*/SKILL.md")):
            text = skill_path.read_text(encoding="utf-8")
            fields = parse_front_matter(text)
            if fields is None:
                all_errors.append(f"{skill_path}: no front matter found")
                continue
            counts["skills"] += 1
            all_errors.extend(validate_skill(skill_path, fields))

        for agent_path in sorted(PLUGINS_DIR.glob("*/agents/*.md")):
            text = agent_path.read_text(encoding="utf-8")
            fields = parse_front_matter(text)
            if fields is None:
                all_errors.append(f"{agent_path}: no front matter found")
                continue
            counts["agents"] += 1
            all_errors.extend(validate_agent(agent_path, fields))

    print(
        f"Validated {counts['adrs']} ADR(s), {counts['research']} research doc(s), "
        f"{counts['skills']} skill(s), {counts['agents']} agent(s)"
    )
    return all_errors


def main() -> None:
    errors = collect_and_validate()

    if errors:
        print(f"\n{len(errors)} error(s) found:")
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)
    else:
        print("All frontmatter checks passed.")


if __name__ == "__main__":
    main()
