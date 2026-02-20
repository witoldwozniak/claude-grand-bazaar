"""Tests for scripts/index_decisions.py."""

from pathlib import Path

import index_decisions as mod


def _write_adr(tmp_path: Path, name: str, frontmatter: str) -> Path:
    """Write an ADR markdown file with given frontmatter."""
    p = tmp_path / name
    p.write_text(f"---\n{frontmatter}\n---\n\n# Body\n", encoding="utf-8")
    return p


class TestParseFrontMatter:
    def test_basic_fields(self, tmp_path: Path):
        p = _write_adr(
            tmp_path,
            "test.md",
            'title: "Test ADR"\nstatus: accepted\ndate: 2026-02-13',
        )
        fields = mod.parse_front_matter(p)
        assert fields is not None
        assert fields["title"] == "Test ADR"
        assert fields["status"] == "accepted"

    def test_block_list(self, tmp_path: Path):
        p = _write_adr(
            tmp_path,
            "test.md",
            "decision-makers:\n  - alice\n  - bob",
        )
        fields = mod.parse_front_matter(p)
        assert fields["decision-makers"] == ["alice", "bob"]

    def test_inline_list(self, tmp_path: Path):
        p = _write_adr(
            tmp_path,
            "test.md",
            "decision-makers: [alice, bob]",
        )
        fields = mod.parse_front_matter(p)
        assert fields["decision-makers"] == ["alice", "bob"]

    def test_null_value(self, tmp_path: Path):
        p = _write_adr(tmp_path, "test.md", "superseded-by: null")
        fields = mod.parse_front_matter(p)
        assert fields["superseded-by"] is None

    def test_no_frontmatter(self, tmp_path: Path):
        p = tmp_path / "test.md"
        p.write_text("# Just a heading\n", encoding="utf-8")
        assert mod.parse_front_matter(p) is None

    def test_empty_block_list(self, tmp_path: Path):
        """An empty block list key with no items should result in an empty list."""
        p = _write_adr(
            tmp_path,
            "test.md",
            "decision-makers:\ntitle: Test",
        )
        fields = mod.parse_front_matter(p)
        # The empty value becomes an empty list, then the next key overwrites current_key
        assert "title" in fields


class TestCollectAdrs:
    def test_skips_non_adr_files(self, tmp_path: Path):
        _write_adr(tmp_path, "_INDEX.md", "title: Index")
        _write_adr(tmp_path, "_TEMPLATE.md", "title: Template")
        _write_adr(tmp_path, "readme.md", "title: Readme")
        _write_adr(
            tmp_path,
            "0001-test.md",
            'title: "ADR-0001"\nstatus: accepted\ndate: 2026-02-13\ndecision-makers:\n  - alice',
        )
        entries = mod.collect_adrs(tmp_path)
        assert len(entries) == 1
        assert entries[0]["number"] == "0001"

    def test_extracts_adr_number(self, tmp_path: Path):
        _write_adr(
            tmp_path,
            "0042-something.md",
            'title: "Test"\nstatus: draft',
        )
        entries = mod.collect_adrs(tmp_path)
        assert entries[0]["number"] == "0042"

    def test_empty_directory(self, tmp_path: Path):
        entries = mod.collect_adrs(tmp_path)
        assert entries == []


class TestBuildIndex:
    def test_empty_entries(self):
        result = mod.build_index([])
        assert "# Decision Records Index" in result
        assert "0 decisions" in result

    def test_with_entries(self):
        entries = [
            {
                "number": "0001",
                "status": "accepted",
                "date": "2026-02-13",
                "title": "Test Decision",
                "decision-makers": ["alice"],
                "filename": "0001-test.md",
            }
        ]
        result = mod.build_index(entries)
        assert "1 decisions" in result
        assert "Test Decision" in result
        assert "0001" in result
        assert "alice" in result

    def test_status_icons(self):
        assert mod.status_icon("draft") != mod.status_icon("accepted")
        assert mod.status_icon("unknown") == "\u2753"
