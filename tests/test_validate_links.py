"""Tests for scripts/validate_links.py."""

import sys
from pathlib import Path

import validate_links as mod


class TestIsExternal:
    def test_http(self):
        assert mod.is_external("http://example.com")

    def test_https(self):
        assert mod.is_external("https://example.com")

    def test_mailto(self):
        assert mod.is_external("mailto:user@example.com")

    def test_relative(self):
        assert not mod.is_external("./file.md")

    def test_absolute_path(self):
        assert not mod.is_external("/path/to/file")


class TestIsAnchorOnly:
    def test_anchor(self):
        assert mod.is_anchor_only("#section")

    def test_not_anchor(self):
        assert not mod.is_anchor_only("file.md#section")

    def test_relative(self):
        assert not mod.is_anchor_only("./file.md")


class TestResolveLink:
    def test_valid_link(self, tmp_path: Path):
        target = tmp_path / "target.md"
        target.write_text("# Target", encoding="utf-8")
        source = tmp_path / "source.md"
        source.write_text("", encoding="utf-8")
        assert mod.resolve_link(source, "target.md") is True

    def test_broken_link(self, tmp_path: Path):
        source = tmp_path / "source.md"
        source.write_text("", encoding="utf-8")
        assert mod.resolve_link(source, "nonexistent.md") is False

    def test_link_with_anchor(self, tmp_path: Path):
        target = tmp_path / "target.md"
        target.write_text("# Target", encoding="utf-8")
        source = tmp_path / "source.md"
        source.write_text("", encoding="utf-8")
        assert mod.resolve_link(source, "target.md#section") is True

    def test_pure_anchor(self, tmp_path: Path):
        source = tmp_path / "source.md"
        source.write_text("", encoding="utf-8")
        # Pure anchor after stripping is empty, should return True
        assert mod.resolve_link(source, "#section") is True

    def test_directory_link(self, tmp_path: Path):
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        source = tmp_path / "source.md"
        source.write_text("", encoding="utf-8")
        assert mod.resolve_link(source, "subdir") is True

    def test_relative_path(self, tmp_path: Path):
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        target = subdir / "target.md"
        target.write_text("# Target", encoding="utf-8")
        source = tmp_path / "source.md"
        source.write_text("", encoding="utf-8")
        assert mod.resolve_link(source, "subdir/target.md") is True

    def test_parent_relative_path(self, tmp_path: Path):
        target = tmp_path / "target.md"
        target.write_text("# Target", encoding="utf-8")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        source = subdir / "source.md"
        source.write_text("", encoding="utf-8")
        assert mod.resolve_link(source, "../target.md") is True


class TestLinkExtraction:
    """Test that the LINK_RE regex works correctly."""

    def test_basic_link(self):
        matches = mod.LINK_RE.findall("[text](target.md)")
        assert ("text", "target.md") in matches

    def test_ignores_image_links(self):
        matches = mod.LINK_RE.findall("![alt](image.png)")
        assert len(matches) == 0

    def test_multiple_links_on_line(self):
        matches = mod.LINK_RE.findall("[a](b.md) and [c](d.md)")
        assert len(matches) == 2

    def test_link_with_anchor(self):
        matches = mod.LINK_RE.findall("[text](file.md#section)")
        assert ("text", "file.md#section") in matches


class TestInlineCodeSkipping:
    """Test that links inside inline code spans are ignored."""

    def test_links_in_inline_code_ignored(self, tmp_path: Path, monkeypatch):
        source = tmp_path / "test.md"
        source.write_text(
            "# Doc\n"
            "\n"
            "Cite sources: `[Source Title](url)` for references.\n"
            "\n"
            "[valid](test.md)\n",
            encoding="utf-8",
        )

        monkeypatch.setattr(mod, "SCAN_DIRS", [])
        monkeypatch.setattr(mod, "SCAN_ROOT_GLOBS", [])
        monkeypatch.setattr(
            mod, "collect_markdown_files", lambda: [source]
        )

        import io

        captured = io.StringIO()
        monkeypatch.setattr(sys, "stdout", captured)

        try:
            mod.main()
        except SystemExit:
            output = captured.getvalue()
            assert False, f"main() exited with error. Output:\n{output}"

        output = captured.getvalue()
        assert "Checked 1 internal link(s)" in output


class TestCodeBlockSkipping:
    """Test that links inside fenced code blocks are ignored by main()."""

    def test_links_in_code_blocks_ignored(self, tmp_path: Path, monkeypatch):
        """Links inside ``` blocks should not be checked."""
        source = tmp_path / "test.md"
        source.write_text(
            "# Doc\n"
            "\n"
            "[valid](test.md)\n"
            "\n"
            "```markdown\n"
            "[inside-code](nonexistent.md)\n"
            "```\n"
            "\n"
            "[also-valid](test.md)\n",
            encoding="utf-8",
        )

        # Patch the scan to only look at our tmp_path
        monkeypatch.setattr(mod, "SCAN_DIRS", [])
        monkeypatch.setattr(mod, "SCAN_ROOT_GLOBS", [])
        monkeypatch.setattr(
            mod, "collect_markdown_files", lambda: [source]
        )

        # Run main and check it doesn't exit(1) — the only internal link
        # is [valid](test.md) which resolves to itself
        # [inside-code](nonexistent.md) should be skipped
        import io

        captured = io.StringIO()
        monkeypatch.setattr(sys, "stdout", captured)

        try:
            mod.main()
        except SystemExit:
            output = captured.getvalue()
            assert False, f"main() exited with error. Output:\n{output}"

        output = captured.getvalue()
        assert "Checked 2 internal link(s)" in output
