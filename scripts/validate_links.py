#!/usr/bin/env python3
"""Validate internal markdown links across the repository.

Scans all .md files in docs/, plugins/, and the repository root.
Extracts [text](relative/path) links, ignoring external URLs (http/https)
and anchor-only fragments (#section). Resolves paths relative to the
source file's directory and reports broken links.

Exit 0 if all links resolve, exit 1 if any are broken.
"""

import re
import sys
from pathlib import Path

# Match markdown links: [text](target)
# Excludes image links ![alt](src) by using negative lookbehind
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")

SCAN_DIRS = [Path("docs"), Path("plugins")]
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

    # Recursive scan of docs/ and plugins/
    for scan_dir in SCAN_DIRS:
        if scan_dir.is_dir():
            files.extend(scan_dir.rglob("*.md"))

    return sorted(set(files))


def resolve_link(source: Path, target: str) -> bool:
    """Check if a relative link target resolves to an existing file or directory."""
    # Strip anchor fragment
    path_part = target.split("#")[0]
    if not path_part:
        return True  # Pure anchor link

    resolved = (source.parent / path_part).resolve()
    return resolved.exists()


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
