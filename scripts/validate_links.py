#!/usr/bin/env python3
"""Validate internal markdown links across the repository.

Scans all .md files in docs/, plugins/, and the repository root.
Extracts [text](relative/path) links, ignoring external URLs (http/https)
and anchor-only fragments (#section). Resolves paths relative to the
source file's directory and reports broken links.

Exit 0 if all links resolve, exit 1 if any are broken.
"""

import os
import re
import sys
from pathlib import Path

# Match markdown links: [text](target)
# Excludes image links ![alt](src) by using negative lookbehind
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")

SCAN_DIRS = [Path("docs"), Path("plugins")]
EXCLUDE_DIRS = {Path("docs/ignore")}
SCAN_ROOT_GLOBS = ["*.md"]


def is_external(target: str) -> bool:
    """Check if a link target is an external URL."""
    return target.startswith(("http://", "https://", "mailto:"))


def is_anchor_only(target: str) -> bool:
    """Check if a link target is just a fragment."""
    return target.startswith("#")


def collect_markdown_files() -> list[Path]:
    """Find all markdown files to scan."""
    files: list[Path] = []

    # Root-level markdown files
    for pattern in SCAN_ROOT_GLOBS:
        files.extend(Path(".").glob(pattern))

    # Recursive scan of docs/ and plugins/, skipping excluded directories
    for scan_dir in SCAN_DIRS:
        if scan_dir.is_dir():
            for f in scan_dir.rglob("*.md"):
                if not any(f.is_relative_to(exc) for exc in EXCLUDE_DIRS):
                    files.append(f)

    return sorted(set(files))


def case_sensitive_exists(source_dir: Path, target_str: str) -> bool:
    """Verify each path component matches actual filesystem case.

    On case-insensitive systems (Windows, macOS) Path.exists() returns True
    even when the case doesn't match.  This walks the target path component
    by component and checks each name against the real directory listing,
    catching mismatches that would break on Linux CI.
    """
    current = source_dir.resolve()
    for part in Path(target_str).parts:
        if part == "..":
            current = current.parent
            continue
        if part == ".":
            continue
        try:
            actual_entries = os.listdir(current)
        except OSError:
            return False
        if part not in actual_entries:
            return False
        current = current / part
    return True


def resolve_link(source: Path, target: str) -> bool:
    """Check if a relative link target resolves to an existing file or directory."""
    # Strip anchor fragment
    path_part = target.split("#")[0]
    if not path_part:
        return True  # Pure anchor link

    resolved = (source.parent / path_part).resolve()
    if not resolved.exists():
        return False

    # Case-sensitive check — catches mismatches invisible on Windows/macOS
    return case_sensitive_exists(source.parent, path_part)


def main() -> None:
    files = collect_markdown_files()
    print(f"Scanning {len(files)} markdown file(s) for broken links...")

    broken: list[tuple[Path, int, str, str]] = []
    total_links = 0
    in_code_block: bool = False

    for path in files:
        text = path.read_text(encoding="utf-8")
        in_code_block = False

        for line_num, line in enumerate(text.splitlines(), 1):
            # Track fenced code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Strip inline code spans before matching links
            stripped = re.sub(r"`[^`]+`", "", line)

            for match in LINK_RE.finditer(stripped):
                link_text, target = match.group(1), match.group(2)

                if is_external(target) or is_anchor_only(target):
                    continue

                total_links += 1

                if not resolve_link(path, target):
                    broken.append((path, line_num, link_text, target))

    print(f"Checked {total_links} internal link(s)")

    if broken:
        print(f"\n{len(broken)} broken link(s) found:")
        for path, line_num, text, target in broken:
            print(f"  {path}:{line_num}: [{text}]({target})")
        sys.exit(1)
    else:
        print("All internal links are valid.")


if __name__ == "__main__":
    main()
