#!/usr/bin/env python3
"""
Fetch Claude Code documentation using the official llms.txt index.

Downloads markdown versions of all (or selected) documentation pages
from code.claude.com/docs into a local directory.

Usage:
    python scripts/fetch-claude-code-docs.py                    # fetch all docs
    python scripts/fetch-claude-code-docs.py -o ./docs          # custom output dir
    python scripts/fetch-claude-code-docs.py --only hooks skills plugins  # subset
    python scripts/fetch-claude-code-docs.py --list              # show available pages
    python scripts/fetch-claude-code-docs.py --delay 0.5         # gentle rate limiting
"""

import argparse
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

LLMS_TXT_URL = "https://code.claude.com/docs/llms.txt"


def fetch(url: str) -> str:
    """Fetch a URL and return its text content."""
    req = urllib.request.Request(url, headers={"User-Agent": "claude-code-docs-fetcher/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_llms_txt(text: str) -> list[dict]:
    """Parse llms.txt into a list of {name, url, description} dicts."""
    entries = []
    for line in text.splitlines():
        match = re.match(r"^- \[(.+?)]\((.+?)\):\s*(.+)$", line.strip())
        if match:
            title, url, description = match.groups()
            # Extract path after /en/ and drop .md
            # e.g. https://code.claude.com/docs/en/hooks-guide.md -> hooks-guide
            # e.g. https://code.claude.com/docs/en/sdk/migration-guide.md -> sdk/migration-guide
            path_part = url.split("/en/", 1)[-1].removesuffix(".md")
            name = path_part.replace("/", "--")  # flatten for filtering, keep original for paths
            entries.append({
                "name": name,
                "path": path_part,
                "title": title,
                "url": url,
                "description": description.strip(),
            })
    return entries


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Claude Code documentation from code.claude.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("claude-code-docs"),
        help="Output directory (default: ./claude-code-docs)",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="PAGE",
        help="Only fetch pages whose slug contains one of these terms (e.g. hooks skills plugins)",
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        metavar="PAGE",
        help="Exclude pages whose slug contains one of these terms",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available pages and exit without downloading",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Delay between requests in seconds (default: 0.2)",
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="Also save the raw llms.txt as _index.txt",
    )

    args = parser.parse_args()

    # Fetch and parse the index
    print(f"Fetching index from {LLMS_TXT_URL}...")
    try:
        llms_txt = fetch(LLMS_TXT_URL)
    except urllib.error.URLError as e:
        print(f"Error fetching index: {e}", file=sys.stderr)
        sys.exit(1)

    entries = parse_llms_txt(llms_txt)
    print(f"Found {len(entries)} documentation pages.\n")

    # Filter if requested
    if args.only:
        entries = [e for e in entries if any(term in e["name"] for term in args.only)]
    if args.exclude:
        entries = [e for e in entries if not any(term in e["name"] for term in args.exclude)]

    # List mode
    if args.list:
        max_name = max(len(e["name"]) for e in entries)
        for e in entries:
            print(f"  {e['name']:<{max_name}}  {e['description'][:80]}")
        print(f"\n{len(entries)} pages available.")
        return

    if not entries:
        print("No pages matched your filters.", file=sys.stderr)
        sys.exit(1)

    # Download
    args.output.mkdir(parents=True, exist_ok=True)

    if args.index:
        index_path = args.output / "_index.txt"
        index_path.write_text(llms_txt, encoding="utf-8")
        print(f"Saved index to {index_path}")

    succeeded = 0
    failed = 0

    for i, entry in enumerate(entries, 1):
        # Preserve subdirectory structure (e.g. sdk/migration-guide.md)
        filepath = args.output / f"{entry['path']}.md"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        print(f"[{i}/{len(entries)}] {entry['path']}...", end=" ", flush=True)

        try:
            content = fetch(entry["url"])
            filepath.write_text(content, encoding="utf-8")
            size_kb = len(content.encode("utf-8")) / 1024
            print(f"OK ({size_kb:.1f} KB)")
            succeeded += 1
        except Exception as e:
            print(f"FAILED ({e})")
            failed += 1

        if i < len(entries):
            time.sleep(args.delay)

    # Summary
    print(f"\nDone: {succeeded} downloaded, {failed} failed.")
    print(f"Output: {args.output.resolve()}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
