"""Tests for scripts/index-research.py."""

from datetime import date, timedelta
from pathlib import Path

import index_research as mod


def _write_research(tmp_path: Path, name: str, frontmatter: str) -> Path:
    """Write a research markdown file with given frontmatter."""
    p = tmp_path / name
    p.write_text(f"---\n{frontmatter}\n---\n\n# Body\n", encoding="utf-8")
    return p


class TestParseFrontMatter:
    def test_basic_fields(self, tmp_path: Path):
        p = _write_research(
            tmp_path,
            "test.md",
            'question: "How do hooks work?"\nstatus: active\nstarted: 2026-02-10',
        )
        fields = mod.parse_front_matter(p)
        assert fields is not None
        assert fields["question"] == "How do hooks work?"
        assert fields["status"] == "active"
        assert fields["started"] == "2026-02-10"

    def test_inline_list(self, tmp_path: Path):
        p = _write_research(
            tmp_path, "test.md", "tags: [hooks, claude-code, enforcement]"
        )
        fields = mod.parse_front_matter(p)
        assert fields["tags"] == ["hooks", "claude-code", "enforcement"]

    def test_quoted_values(self, tmp_path: Path):
        p = _write_research(tmp_path, "test.md", "question: \"What is X?\"")
        fields = mod.parse_front_matter(p)
        assert fields["question"] == "What is X?"

    def test_single_quoted_values(self, tmp_path: Path):
        p = _write_research(tmp_path, "test.md", "question: 'What is X?'")
        fields = mod.parse_front_matter(p)
        assert fields["question"] == "What is X?"

    def test_null_value(self, tmp_path: Path):
        p = _write_research(tmp_path, "test.md", "concluded: null")
        fields = mod.parse_front_matter(p)
        assert fields["concluded"] is None

    def test_no_frontmatter(self, tmp_path: Path):
        p = tmp_path / "test.md"
        p.write_text("# Just a heading\n", encoding="utf-8")
        assert mod.parse_front_matter(p) is None

    def test_empty_list(self, tmp_path: Path):
        p = _write_research(tmp_path, "test.md", "tags: []")
        fields = mod.parse_front_matter(p)
        assert fields["tags"] == []

    def test_list_with_quoted_items(self, tmp_path: Path):
        p = _write_research(tmp_path, "test.md", 'tags: ["hooks", "code"]')
        fields = mod.parse_front_matter(p)
        assert fields["tags"] == ["hooks", "code"]


class TestCheckStaleness:
    def test_concluded_becomes_stale(self, tmp_path: Path):
        concluded_date = date.today() - timedelta(days=100)
        p = _write_research(
            tmp_path,
            "test.md",
            f"status: concluded\nconcluded: {concluded_date}\nstale_after: 90",
        )
        entry = {"status": "concluded", "concluded": str(concluded_date), "stale_after": "90"}
        changed = mod.check_staleness(entry, p, date.today())
        assert changed is True
        assert entry["status"] == "stale"
        assert "status: stale" in p.read_text(encoding="utf-8")

    def test_concluded_not_yet_stale(self, tmp_path: Path):
        concluded_date = date.today() - timedelta(days=30)
        p = _write_research(
            tmp_path,
            "test.md",
            f"status: concluded\nconcluded: {concluded_date}\nstale_after: 90",
        )
        entry = {"status": "concluded", "concluded": str(concluded_date), "stale_after": "90"}
        changed = mod.check_staleness(entry, p, date.today())
        assert changed is False
        assert entry["status"] == "concluded"

    def test_non_concluded_skipped(self, tmp_path: Path):
        p = _write_research(tmp_path, "test.md", "status: active")
        entry = {"status": "active"}
        changed = mod.check_staleness(entry, p, date.today())
        assert changed is False

    def test_no_concluded_date_skipped(self, tmp_path: Path):
        p = _write_research(tmp_path, "test.md", "status: concluded\nconcluded: null")
        entry = {"status": "concluded", "concluded": None}
        changed = mod.check_staleness(entry, p, date.today())
        assert changed is False

    def test_default_stale_after(self, tmp_path: Path):
        concluded_date = date.today() - timedelta(days=91)
        p = _write_research(
            tmp_path,
            "test.md",
            f"status: concluded\nconcluded: {concluded_date}",
        )
        entry = {"status": "concluded", "concluded": str(concluded_date)}
        changed = mod.check_staleness(entry, p, date.today())
        assert changed is True


class TestCollectResearch:
    def test_skips_index_and_templates(self, tmp_path: Path):
        _write_research(tmp_path, "_INDEX.md", "question: skip")
        _write_research(tmp_path, "_TEMPLATE.md", "question: skip")
        _write_research(tmp_path, "_GUIDE.md", "question: skip")
        _write_research(
            tmp_path,
            "2026-02-10-real.md",
            'question: "Real question"\nstatus: active\nstarted: 2026-02-10',
        )
        entries = mod.collect_research(tmp_path, date.today())
        assert len(entries) == 1
        assert entries[0]["question"] == "Real question"

    def test_empty_directory(self, tmp_path: Path):
        entries = mod.collect_research(tmp_path, date.today())
        assert entries == []


class TestBuildIndex:
    def test_empty_entries(self):
        result = mod.build_index([])
        assert "# Research Index" in result
        assert "0 documents" in result

    def test_with_entries(self):
        entries = [
            {
                "status": "active",
                "started": "2026-02-10",
                "question": "How do hooks work?",
                "tags": ["hooks"],
                "filename": "2026-02-10-hooks.md",
            }
        ]
        result = mod.build_index(entries)
        assert "1 documents" in result
        assert "How do hooks work?" in result
        assert "`hooks`" in result
        assert "## By Tag" in result

    def test_tag_index(self):
        entries = [
            {
                "status": "active",
                "started": "2026-02-10",
                "question": "Q1",
                "tags": ["a", "b"],
                "filename": "q1.md",
            },
            {
                "status": "draft",
                "started": "2026-02-11",
                "question": "Q2",
                "tags": ["b", "c"],
                "filename": "q2.md",
            },
        ]
        result = mod.build_index(entries)
        assert "**a**" in result
        assert "**b**" in result
        assert "**c**" in result
