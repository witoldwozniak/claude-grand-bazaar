#!/usr/bin/env python3
"""Sync GitHub labels for the Grand Bazaar.

Creates and updates labels for PDLC stages, general-purpose categories,
and plugin-specific labels derived from marketplace.json.

Idempotent: creates missing labels, updates drifted color/description,
never deletes. Requires `gh` CLI authenticated.

Usage:
    python scripts/sync_labels.py              # create/update all labels
    python scripts/sync_labels.py --dry-run    # preview without changes
    python scripts/sync_labels.py --plugin foo # also create plugin/foo label
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

MARKETPLACE_PATH = Path(".claude-plugin/marketplace.json")

# Static labels: (name, description, color without #)
STATIC_LABELS: list[tuple[str, str, str]] = [
    # PDLC stage labels — light-to-dark purple gradient
    ("stage/concept", "PDLC Stage 1: Define scope and ambition", "e8d5f5"),
    ("stage/research", "PDLC Stage 2: Study the domain", "d4b8e8"),
    ("stage/design", "PDLC Stage 3: Make opinionated choices", "c09bdb"),
    ("stage/build", "PDLC Stage 4: Implement the plugin", "ac7ece"),
    ("stage/prove", "PDLC Stage 5: Test in real work", "9861c1"),
    ("stage/review", "PDLC Stage 6: Structured self-review", "8444b4"),
    ("stage/document", "PDLC Stage 7: Write for the stranger", "7027a7"),
    ("stage/ship", "PDLC Stage 8: Put it on the shelves", "5c0a9a"),
    ("stage/maintenance", "PDLC Stage 9: Ongoing post-ship care", "480a8d"),
    # General-purpose labels
    ("plugin-proposal", "A new plugin proposed for the Bazaar", "0e8a16"),
    ("bug", "Something is broken", "d73a4a"),
    ("enhancement", "New feature or improvement", "a2eeef"),
    ("maintenance", "Dependency updates, cleanup, CI/CD", "f9d0c4"),
    ("research", "Standalone research spike", "1d76db"),
    ("blocked", "Waiting on external dependency or decision", "b60205"),
    ("needs-code-actual", "Requires human decision before proceeding", "ff7619"),
]

PLUGIN_LABEL_COLOR = "fbca04"


def check_gh_auth() -> bool:
    """Verify gh CLI is authenticated."""
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def get_existing_labels() -> dict[str, dict[str, str]]:
    """Fetch all existing labels from the repo. Returns {name: {description, color}}."""
    result = subprocess.run(
        ["gh", "label", "list", "--limit", "200", "--json", "name,description,color"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"error: failed to list labels: {result.stderr.strip()}")
        sys.exit(1)

    labels = json.loads(result.stdout)
    return {
        label["name"]: {
            "description": label.get("description", ""),
            "color": label.get("color", "").lstrip("#"),
        }
        for label in labels
    }


def create_label(name: str, description: str, color: str, dry_run: bool) -> None:
    """Create a new label."""
    if dry_run:
        print(f"  [dry-run] would CREATE: {name} (#{color}) — {description}")
        return

    result = subprocess.run(
        [
            "gh", "label", "create", name,
            "--description", description,
            "--color", color,
            "--force",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ERROR creating {name}: {result.stderr.strip()}")
    else:
        print(f"  CREATED: {name}")


def update_label(name: str, description: str, color: str, dry_run: bool) -> None:
    """Update an existing label's description and/or color."""
    if dry_run:
        print(f"  [dry-run] would UPDATE: {name} (#{color}) — {description}")
        return

    result = subprocess.run(
        [
            "gh", "label", "edit", name,
            "--description", description,
            "--color", color,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ERROR updating {name}: {result.stderr.strip()}")
    else:
        print(f"  UPDATED: {name}")


def sync_label(
    name: str,
    description: str,
    color: str,
    existing: dict[str, dict[str, str]],
    dry_run: bool,
) -> None:
    """Create or update a single label as needed."""
    color = color.lstrip("#")

    if name not in existing:
        create_label(name, description, color, dry_run)
        return

    current = existing[name]
    needs_update = (
        current["color"].lower() != color.lower()
        or current["description"] != description
    )

    if needs_update:
        update_label(name, description, color, dry_run)
    else:
        print(f"  OK: {name}")


def load_plugin_names() -> list[str]:
    """Read plugin names from marketplace.json."""
    if not MARKETPLACE_PATH.is_file():
        print(f"warning: {MARKETPLACE_PATH} not found, skipping dynamic plugin labels")
        return []

    try:
        data = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"warning: {MARKETPLACE_PATH} is not valid JSON: {e}")
        return []

    plugins = data.get("plugins", [])
    return [p["name"] for p in plugins if "name" in p]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync GitHub labels for the Grand Bazaar."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without creating or updating labels.",
    )
    parser.add_argument(
        "--plugin",
        action="append",
        default=[],
        metavar="NAME",
        help="Additional plugin/<name> label to create (repeatable).",
    )
    args = parser.parse_args()

    # Check gh auth
    print("Checking gh CLI authentication...")
    if not check_gh_auth():
        print("error: gh CLI is not authenticated. Run `gh auth login` first.")
        sys.exit(1)
    print("  Authenticated.\n")

    # Fetch existing labels
    print("Fetching existing labels...")
    existing = get_existing_labels()
    print(f"  Found {len(existing)} existing label(s).\n")

    # Sync static labels
    print("Syncing static labels...")
    for name, description, color in STATIC_LABELS:
        sync_label(name, description, color, existing, args.dry_run)

    # Build dynamic plugin labels
    plugin_names = load_plugin_names()
    for extra in args.plugin:
        if extra not in plugin_names:
            plugin_names.append(extra)

    if plugin_names:
        print(f"\nSyncing plugin labels ({len(plugin_names)})...")
        for name in sorted(plugin_names):
            label_name = f"plugin/{name}"
            description = f"Plugin: {name}"
            sync_label(label_name, description, PLUGIN_LABEL_COLOR, existing, args.dry_run)
    else:
        print("\nNo plugin labels to sync.")

    print("\nDone.")


if __name__ == "__main__":
    main()
