#!/usr/bin/env python3
"""
Initialize a new subagent with proper structure and templates.

Usage:
    python init_subagent.py <subagent-name> --path <output-directory>

Examples:
    python init_subagent.py code-reviewer --path .claude/agents
    python init_subagent.py test-runner --path ~/.claude/agents
"""

import argparse
import sys
from pathlib import Path


def validate_name(name: str) -> bool:
    """Validate subagent name follows conventions."""
    if not name:
        return False
    
    # Must be lowercase with hyphens only
    if not all(c.islower() or c.isdigit() or c == '-' for c in name):
        return False
    
    # Must start with a letter
    if not name[0].islower():
        return False
    
    # Can't end with hyphen
    if name.endswith('-'):
        return False
    
    # No consecutive hyphens
    if '--' in name:
        return False
    
    return True


def create_subagent_template(name: str, output_path: Path) -> None:
    """Create a new subagent template file."""
    
    if not validate_name(name):
        print(f"Error: Invalid subagent name '{name}'")
        print("Subagent names must be:")
        print("  - Lowercase letters, numbers, and hyphens only")
        print("  - Start with a letter")
        print("  - Not end with a hyphen")
        print("  - No consecutive hyphens")
        print("Examples: code-reviewer, test-runner, data-analyst")
        sys.exit(1)
    
    # Expand user home directory
    output_path = output_path.expanduser()
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create subagent file
    subagent_file = output_path / f"{name}.md"
    
    if subagent_file.exists():
        print(f"Error: Subagent file already exists: {subagent_file}")
        sys.exit(1)
    
    # Generate template content
    template = f"""---
name: {name}
description: TODO: Describe when this subagent should be invoked. Include trigger words like "PROACTIVELY", "Use when", or "MUST BE USED" for automatic delegation.
tools: Read, Grep, Glob, Bash
# disallowedTools: Delete
model: sonnet
# permissionMode: default
# skills: skill-name
# memory: project
# mcpServers:
#   server-name:
#     command: npx
#     args: ["-y", "@org/server-package"]
# maxTurns: 50
# hooks:
#   PreToolUse:
#     - matcher: "Bash"
#       hooks:
#         - type: command
#           command: "./scripts/validate.sh"
---

You are a [TODO: role description] specializing in [TODO: domain].

When invoked:
1. TODO: First step
2. TODO: Second step
3. TODO: Third step

[TODO: Task name] checklist:
- TODO: Item 1
- TODO: Item 2
- TODO: Item 3

Provide [TODO: output format]:
- TODO: Structure 1
- TODO: Structure 2
- TODO: Structure 3

[TODO: Add constraints or things to avoid]
"""
    
    # Write template
    subagent_file.write_text(template)
    
    print(f"✓ Created subagent template: {subagent_file}")
    print()
    print("Next steps:")
    print(f"1. Edit {subagent_file}")
    print("2. Replace all TODO markers with actual content")
    print("3. Customize the system prompt for your use case")
    print("4. Uncomment and configure optional fields as needed")
    print("5. Test the subagent with real tasks")
    print()
    print("To load immediately: use /agents command")
    print("Otherwise: restart Claude Code for changes to take effect")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new subagent with proper structure"
    )
    parser.add_argument(
        "name",
        help="Subagent name (lowercase with hyphens, e.g., 'code-reviewer')"
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path(".claude/agents"),
        help="Output directory path (default: .claude/agents)"
    )
    
    args = parser.parse_args()
    
    create_subagent_template(args.name, args.path)


if __name__ == "__main__":
    main()
