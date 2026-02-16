#!/usr/bin/env python3
"""Validate marketplace.json and all plugin.json manifests.

Checks:
- marketplace.json has required top-level fields
- Each plugin's source directory exists under plugins/
- Each plugin has .claude-plugin/plugin.json with required fields
- Plugin name in plugin.json matches directory name
- Versions are valid semver (X.Y.Z)

Exit 0 if all checks pass, exit 1 if any fail.
"""

import json
import re
import sys
from pathlib import Path

MARKETPLACE_PATH = Path(".claude-plugin/marketplace.json")
PLUGINS_DIR = Path("plugins")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

MARKETPLACE_REQUIRED = {"name", "owner", "metadata", "plugins"}
PLUGIN_REQUIRED = {"name", "version", "description", "author", "license"}


def error(msg: str) -> None:
    print(f"  ERROR: {msg}")


def validate_marketplace(data: dict) -> list[str]:
    """Validate marketplace.json structure. Returns list of errors."""
    errors = []
    missing = MARKETPLACE_REQUIRED - set(data.keys())
    if missing:
        errors.append(f"marketplace.json missing required fields: {', '.join(sorted(missing))}")

    plugins = data.get("plugins")
    if plugins is not None and not isinstance(plugins, list):
        errors.append("marketplace.json 'plugins' must be an array")

    metadata = data.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        errors.append("marketplace.json 'metadata' must be an object")

    return errors


def validate_plugin_entry(entry: dict, index: int) -> list[str]:
    """Validate a single plugin entry in marketplace.json."""
    errors = []
    name = entry.get("name")
    source = entry.get("source")

    if not name:
        errors.append(f"plugins[{index}]: missing 'name'")
    if not source:
        errors.append(f"plugins[{index}]: missing 'source'")
        return errors

    plugin_dir = PLUGINS_DIR / source
    if not plugin_dir.is_dir():
        errors.append(f"plugins[{index}] ({name}): source directory '{plugin_dir}' does not exist")
        return errors

    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest_path.is_file():
        errors.append(f"plugins[{index}] ({name}): missing {manifest_path}")
        return errors

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"plugins[{index}] ({name}): invalid JSON in {manifest_path}: {e}")
        return errors

    missing = PLUGIN_REQUIRED - set(manifest.keys())
    if missing:
        errors.append(
            f"plugins[{index}] ({name}): {manifest_path} missing required fields: "
            f"{', '.join(sorted(missing))}"
        )

    # Name must match directory name
    manifest_name = manifest.get("name")
    if manifest_name and manifest_name != source:
        errors.append(
            f"plugins[{index}] ({name}): plugin.json name '{manifest_name}' "
            f"does not match directory name '{source}'"
        )

    # Version must be valid semver
    version = manifest.get("version")
    if version and not SEMVER_RE.match(str(version)):
        errors.append(
            f"plugins[{index}] ({name}): version '{version}' is not valid semver (expected X.Y.Z)"
        )

    return errors


def main() -> None:
    all_errors: list[str] = []

    if not MARKETPLACE_PATH.is_file():
        print(f"error: {MARKETPLACE_PATH} not found")
        sys.exit(1)

    try:
        data = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"error: {MARKETPLACE_PATH} is not valid JSON: {e}")
        sys.exit(1)

    print(f"Validating {MARKETPLACE_PATH}...")
    all_errors.extend(validate_marketplace(data))

    plugins = data.get("plugins", [])
    print(f"Found {len(plugins)} plugin(s) in marketplace")

    for i, entry in enumerate(plugins):
        all_errors.extend(validate_plugin_entry(entry, i))

    if all_errors:
        print(f"\n{len(all_errors)} error(s) found:")
        for e in all_errors:
            error(e)
        sys.exit(1)
    else:
        print("All manifest checks passed.")


if __name__ == "__main__":
    main()
