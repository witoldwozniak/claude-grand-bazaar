#!/usr/bin/env python3
"""
Validate subagent file format and content.

Usage:
    python validate_subagent.py <path-to-subagent.md>

Examples:
    python validate_subagent.py .claude/agents/code-reviewer.md
    python validate_subagent.py ~/.claude/agents/test-runner.md
"""

import argparse
import re
import sys
from pathlib import Path


class ValidationError(Exception):
    """Validation error with severity level."""
    def __init__(self, message: str, severity: str = "error"):
        self.message = message
        self.severity = severity
        super().__init__(message)


VALID_TOOLS = [
    "Read", "Write", "Edit", "Grep", "Glob", "Bash", "Delete"
]

VALID_MODELS = ["sonnet", "opus", "haiku", "inherit"]

VALID_PERMISSION_MODES = [
    "default", "acceptEdits", "delegate", "dontAsk", "bypassPermissions", "plan"
]

TRIGGER_WORDS = [
    "proactively", "use when", "must be used", "immediately", "use for"
]


def parse_frontmatter(content: str) -> tuple[dict, str, list[ValidationError]]:
    """Parse YAML frontmatter and return fields, body, and any parsing errors."""
    errors = []
    
    if not content.startswith("---\n"):
        errors.append(ValidationError("Missing YAML frontmatter (must start with ---)"))
        return {}, content, errors
    
    try:
        _, frontmatter, body = content.split("---\n", 2)
    except ValueError:
        errors.append(ValidationError("Invalid YAML frontmatter format (missing closing ---)"))
        return {}, content, errors
    
    # Parse frontmatter fields (simple YAML parsing)
    fields = {}
    current_key = None
    
    for line in frontmatter.strip().split("\n"):
        # Skip comments
        if line.strip().startswith("#"):
            continue
        
        # Skip empty lines
        if not line.strip():
            continue
        
        # Check for key-value pair
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            
            # Handle multi-line values (hooks, etc.)
            if not value:
                fields[key] = {}
                current_key = key
            else:
                fields[key] = value
                current_key = None
    
    return fields, body.strip(), errors


def validate_name(name: str) -> list[ValidationError]:
    """Validate the name field."""
    errors = []
    
    if not name:
        errors.append(ValidationError("Missing required field: name"))
        return errors
    
    # Must be lowercase letters, numbers, hyphens only
    if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', name) and len(name) > 1:
        errors.append(ValidationError(
            f"Invalid name format: '{name}'. Must be lowercase with hyphens only, "
            "start with a letter, and not end with hyphen"
        ))
    elif len(name) == 1 and not name.islower():
        errors.append(ValidationError(
            f"Invalid name format: '{name}'. Single character names must be lowercase letters"
        ))
    
    # Check for consecutive hyphens
    if "--" in name:
        errors.append(ValidationError(
            f"Invalid name: '{name}'. No consecutive hyphens allowed"
        ))
    
    return errors


def validate_description(desc: str) -> list[ValidationError]:
    """Validate the description field."""
    errors = []
    
    if not desc:
        errors.append(ValidationError("Missing required field: description"))
        return errors
    
    if len(desc) < 20:
        errors.append(ValidationError(
            f"Description too short ({len(desc)} chars). Should be at least 20 characters.",
            severity="warning"
        ))
    
    # Check for trigger words
    has_trigger = any(word in desc.lower() for word in TRIGGER_WORDS)
    if not has_trigger:
        errors.append(ValidationError(
            "Description should include trigger words for automatic delegation "
            "(e.g., 'PROACTIVELY', 'Use when', 'MUST BE USED', 'Use for')",
            severity="warning"
        ))
    
    return errors


def validate_tools(tools_str: str) -> list[ValidationError]:
    """Validate the tools field."""
    errors = []
    
    if not tools_str:
        return errors  # Optional field
    
    tools = [t.strip() for t in tools_str.split(",")]
    
    for tool in tools:
        if tool not in VALID_TOOLS:
            # Could be an MCP tool, just warn
            errors.append(ValidationError(
                f"Unknown tool: '{tool}'. Standard tools: {', '.join(VALID_TOOLS)}. "
                "This may be valid if it's an MCP tool.",
                severity="warning"
            ))
    
    return errors


def validate_disallowed_tools(tools_str: str) -> list[ValidationError]:
    """Validate the disallowedTools field."""
    errors = []
    
    if not tools_str:
        return errors  # Optional field
    
    tools = [t.strip() for t in tools_str.split(",")]
    
    for tool in tools:
        if tool not in VALID_TOOLS:
            errors.append(ValidationError(
                f"Unknown disallowed tool: '{tool}'. Standard tools: {', '.join(VALID_TOOLS)}",
                severity="warning"
            ))
    
    return errors


def validate_model(model: str) -> list[ValidationError]:
    """Validate the model field."""
    errors = []
    
    if not model:
        return errors  # Optional field, defaults to sonnet
    
    if model not in VALID_MODELS:
        errors.append(ValidationError(
            f"Invalid model: '{model}'. Valid models: {', '.join(VALID_MODELS)}"
        ))
    
    return errors


def validate_permission_mode(mode: str) -> list[ValidationError]:
    """Validate the permissionMode field."""
    errors = []
    
    if not mode:
        return errors  # Optional field
    
    if mode not in VALID_PERMISSION_MODES:
        errors.append(ValidationError(
            f"Invalid permissionMode: '{mode}'. Valid modes: {', '.join(VALID_PERMISSION_MODES)}"
        ))
    
    return errors


def validate_body(body: str) -> list[ValidationError]:
    """Validate the system prompt body."""
    errors = []
    
    if not body:
        errors.append(ValidationError("Empty system prompt. Add instructions for the subagent."))
        return errors
    
    if len(body) < 100:
        errors.append(ValidationError(
            f"System prompt is very short ({len(body)} chars). Add more detailed instructions.",
            severity="warning"
        ))
    
    # Check for TODO markers
    if "TODO" in body:
        todo_count = body.count("TODO")
        errors.append(ValidationError(
            f"Found {todo_count} TODO marker(s) in system prompt. Replace with actual content.",
            severity="warning"
        ))
    
    # Check for common structure elements
    if "when invoked" not in body.lower():
        errors.append(ValidationError(
            "Consider adding a 'When invoked:' section to clarify immediate actions.",
            severity="warning"
        ))
    
    return errors


def validate_subagent(file_path: Path) -> list[ValidationError]:
    """Validate a subagent file and return list of errors/warnings."""
    errors = []
    
    # Expand user home directory
    file_path = file_path.expanduser()
    
    if not file_path.exists():
        errors.append(ValidationError(f"File not found: {file_path}"))
        return errors
    
    if not file_path.suffix == ".md":
        errors.append(ValidationError(
            f"Subagent files should have .md extension, got: {file_path.suffix}",
            severity="warning"
        ))
    
    content = file_path.read_text()
    
    # Parse frontmatter
    fields, body, parse_errors = parse_frontmatter(content)
    errors.extend(parse_errors)
    
    if parse_errors and any(e.severity == "error" for e in parse_errors):
        return errors
    
    # Validate individual fields
    errors.extend(validate_name(fields.get("name", "")))
    errors.extend(validate_description(fields.get("description", "")))
    errors.extend(validate_tools(fields.get("tools", "")))
    errors.extend(validate_disallowed_tools(fields.get("disallowedTools", "")))
    errors.extend(validate_model(fields.get("model", "")))
    errors.extend(validate_permission_mode(fields.get("permissionMode", "")))
    errors.extend(validate_body(body))
    
    # Check for conflicting tools
    if fields.get("tools") and fields.get("disallowedTools"):
        tools = set(t.strip() for t in fields["tools"].split(","))
        disallowed = set(t.strip() for t in fields["disallowedTools"].split(","))
        overlap = tools & disallowed
        if overlap:
            errors.append(ValidationError(
                f"Tools appear in both tools and disallowedTools: {', '.join(overlap)}",
                severity="warning"
            ))
    
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate subagent file format and content"
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to subagent markdown file"
    )
    
    args = parser.parse_args()
    
    print(f"Validating: {args.file}\n")
    
    errors = validate_subagent(args.file)
    
    if not errors:
        print("✓ Subagent validation passed!")
        return 0
    
    # Separate errors and warnings
    critical_errors = [e for e in errors if e.severity == "error"]
    warnings = [e for e in errors if e.severity == "warning"]
    
    if critical_errors:
        print("ERRORS:")
        for error in critical_errors:
            print(f"  ✗ {error.message}")
        print()
    
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  ⚠ {warning.message}")
        print()
    
    if critical_errors:
        print("Validation failed. Fix errors before using this subagent.")
        return 1
    else:
        print("Validation passed with warnings. Consider addressing them.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
