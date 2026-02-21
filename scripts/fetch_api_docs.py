#!/usr/bin/env python3
"""
Fetch Claude API documentation using the official llms.txt index.

Downloads markdown versions of all (or selected) documentation pages
from platform.claude.com into a local directory. Only fetches English
(/en/) pages.

Usage:
    python scripts/fetch_api_docs.py                          # fetch all docs
    python scripts/fetch_api_docs.py -o ./docs                # custom output dir
    python scripts/fetch_api_docs.py --only prompt-engineering agent-sdk  # subset
    python scripts/fetch_api_docs.py --list                   # show available pages
    python scripts/fetch_api_docs.py --delay 0.5              # gentle rate limiting
"""

import argparse
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

LLMS_TXT_URL = "https://platform.claude.com/llms.txt"


def fetch(url: str) -> str:
    """Fetch a URL and return its text content."""
    req = urllib.request.Request(url, headers={"User-Agent": "claude-api-docs-fetcher/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_llms_txt(text: str) -> list[dict]:
    """Parse llms.txt into a list of {name, url, description} dicts.

    Only includes English (/en/) pages. Handles the platform.claude.com
    format where description is optional:
        - [Title](URL) - Description
        - [Title](URL)
    """
    entries = []
    for line in text.splitlines():
        match = re.match(r"^- \[(.+?)]\((.+?)\)(?:\s+-\s+(.+))?$", line.strip())
        if match:
            title, url, description = match.groups()
            # Only include English pages
            if "/en/" not in url:
                continue
            # Extract path after /en/ and drop .md
            # e.g. https://platform.claude.com/docs/en/build-with-claude/tool-use/overview.md
            #   -> build-with-claude/tool-use/overview
            path_part = url.split("/en/", 1)[-1].removesuffix(".md")
            name = path_part.replace("/", "--")  # flatten for filtering
            entries.append({
                "name": name,
                "path": path_part,
                "title": title,
                "url": url,
                "description": (description or "").strip(),
            })
    return entries


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Claude API documentation from platform.claude.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("docs/api-docs"),
        help="Output directory (default: docs/api-docs)",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="PAGE",
        help="Only fetch pages whose slug contains one of these terms (e.g. prompt-engineering agent-sdk)",
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
    except (urllib.error.URLError, OSError, UnicodeDecodeError) as e:
        print(f"Error fetching index: {e}", file=sys.stderr)
        sys.exit(1)

    entries = parse_llms_txt(llms_txt)
    print(f"Found {len(entries)} English documentation pages.\n")

    # Filter if requested
    if args.only:
        entries = [e for e in entries if any(term in e["name"] for term in args.only)]
    if args.exclude:
        entries = [e for e in entries if not any(term in e["name"] for term in args.exclude)]

    if not entries:
        print("No pages matched your filters.", file=sys.stderr)
        sys.exit(1)

    # List mode
    if args.list:
        max_name = max(len(e["name"]) for e in entries)
        for e in entries:
            desc = e["description"][:80] if e["description"] else "(no description)"
            print(f"  {e['name']:<{max_name}}  {desc}")
        print(f"\n{len(entries)} pages available.")
        return

    # Download
    args.output.mkdir(parents=True, exist_ok=True)

    if args.index:
        index_path = args.output / "_index.txt"
        index_path.write_text(llms_txt, encoding="utf-8")
        print(f"Saved index to {index_path}")

    succeeded = 0
    failed = 0

    for i, entry in enumerate(entries, 1):
        # Preserve subdirectory structure
        filepath = args.output / f"{entry['path']}.md"
        if not filepath.resolve().is_relative_to(args.output.resolve()):
            print(f"SKIPPED (path outside output directory: {entry['path']})")
            failed += 1
            continue
        filepath.parent.mkdir(parents=True, exist_ok=True)
        print(f"[{i}/{len(entries)}] {entry['path']}...", end=" ", flush=True)

        try:
            content = fetch(entry["url"])
        except (urllib.error.URLError, OSError) as e:
            print(f"FAILED ({e})")
            failed += 1
            if i < len(entries):
                time.sleep(args.delay)
            continue

        try:
            filepath.write_text(content, encoding="utf-8")
        except OSError as e:
            print(f"WRITE FAILED ({e})")
            failed += 1
            if i < len(entries):
                time.sleep(args.delay)
            continue

        size_kb = len(content.encode("utf-8")) / 1024
        print(f"OK ({size_kb:.1f} KB)")
        succeeded += 1

        if i < len(entries):
            time.sleep(args.delay)

    # Summary
    print(f"\nDone: {succeeded} downloaded, {failed} failed.")
    print(f"Output: {args.output.resolve()}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
