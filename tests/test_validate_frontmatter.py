"""Tests for scripts/validate_frontmatter.py."""

from pathlib import Path

import validate_frontmatter as mod


class TestParseFrontMatter:
    def test_basic_fields(self):
        text = '---\ntitle: "Test"\nstatus: accepted\n---\n# Body\n'
        fields = mod.parse_front_matter(text)
        assert fields is not None
        assert fields["title"] == "Test"
        assert fields["status"] == "accepted"

    def test_multiline_scalar(self):
        text = "---\ndescription: |\n  Line one\n  Line two\nname: test\n---\n"
        fields = mod.parse_front_matter(text)
        assert fields is not None
        assert "Line one" in fields["description"]
        assert "Line two" in fields["description"]
        assert fields["name"] == "test"

    def test_block_list(self):
        text = "---\ndecision-makers:\n  - alice\n  - bob\n---\n"
        fields = mod.parse_front_matter(text)
        assert fields["decision-makers"] == ["alice", "bob"]

    def test_inline_list(self):
        text = "---\ntags: [hooks, code]\n---\n"
        fields = mod.parse_front_matter(text)
        assert fields["tags"] == ["hooks", "code"]

    def test_null(self):
        text = "---\nconcluded: null\n---\n"
        fields = mod.parse_front_matter(text)
        assert fields["concluded"] is None

    def test_no_frontmatter(self):
        text = "# Just a heading\n"
        assert mod.parse_front_matter(text) is None


class TestValidateAdr:
    def _path(self, name: str = "0001-test.md") -> Path:
        return Path("docs/decisions") / name

    def test_valid_adr(self):
        fields = {
            "title": "Test",
            "status": "accepted",
            "date": "2026-02-13",
            "decision-makers": ["alice"],
        }
        errors = mod.validate_adr(self._path(), fields)
        assert errors == []

    def test_missing_required_fields(self):
        errors = mod.validate_adr(self._path(), {})
        assert len(errors) == 4

    def test_invalid_status(self):
        fields = {
            "title": "Test",
            "status": "invalid",
            "date": "2026-02-13",
            "decision-makers": ["alice"],
        }
        errors = mod.validate_adr(self._path(), fields)
        assert any("invalid status" in e for e in errors)

    def test_invalid_date(self):
        fields = {
            "title": "Test",
            "status": "accepted",
            "date": "Feb 13",
            "decision-makers": ["alice"],
        }
        errors = mod.validate_adr(self._path(), fields)
        assert any("invalid date" in e for e in errors)

    def test_all_valid_statuses(self):
        for status in mod.ADR_STATUSES:
            fields = {
                "title": "Test",
                "status": status,
                "date": "2026-02-13",
                "decision-makers": ["alice"],
            }
            errors = mod.validate_adr(self._path(), fields)
            assert not any("invalid status" in e for e in errors)

    def test_impossible_date(self):
        fields = {
            "title": "Test",
            "status": "accepted",
            "date": "2026-02-30",
            "decision-makers": ["alice"],
        }
        errors = mod.validate_adr(self._path(), fields)
        assert any("invalid date" in e for e in errors)


class TestValidateResearch:
    def _path(self, name: str = "2026-02-10-test.md") -> Path:
        return Path("docs/research") / name

    def test_valid_research(self):
        fields = {
            "question": "How?",
            "status": "active",
            "started": "2026-02-10",
            "tags": ["hooks"],
        }
        errors = mod.validate_research(self._path(), fields)
        assert errors == []

    def test_missing_required_fields(self):
        errors = mod.validate_research(self._path(), {})
        assert len(errors) == 4

    def test_invalid_status(self):
        fields = {
            "question": "Q",
            "status": "invalid",
            "started": "2026-02-10",
            "tags": ["x"],
        }
        errors = mod.validate_research(self._path(), fields)
        assert any("invalid status" in e for e in errors)

    def test_all_valid_statuses(self):
        for status in mod.RESEARCH_STATUSES:
            fields = {
                "question": "Q",
                "status": status,
                "started": "2026-02-10",
                "tags": ["x"],
            }
            errors = mod.validate_research(self._path(), fields)
            assert not any("invalid status" in e for e in errors)

    def test_invalid_started_date(self):
        fields = {
            "question": "Q",
            "status": "active",
            "started": "February",
            "tags": ["x"],
        }
        errors = mod.validate_research(self._path(), fields)
        assert any("invalid started date" in e for e in errors)

    def test_missing_tags(self):
        fields = {"question": "Q", "status": "active", "started": "2026-02-10"}
        errors = mod.validate_research(self._path(), fields)
        assert any("'tags'" in e for e in errors)


class TestValidateSkill:
    def _path(self) -> Path:
        return Path("plugins/test/skills/my-skill/SKILL.md")

    def test_valid_skill(self):
        fields = {"name": "my-skill", "description": "A test skill"}
        errors = mod.validate_skill(self._path(), fields)
        assert errors == []

    def test_missing_required_fields(self):
        errors = mod.validate_skill(self._path(), {})
        assert len(errors) == 2

    def test_non_kebab_name(self):
        fields = {"name": "MySkill", "description": "A test skill"}
        errors = mod.validate_skill(self._path(), fields)
        assert any("not kebab-case" in e for e in errors)

    def test_kebab_case_variants(self):
        valid = ["my-skill", "a", "skill-v2", "a-b-c"]
        invalid = ["MySkill", "my_skill", "MY-SKILL", "-leading", "trailing-", "1-starts-with-digit"]
        for name in valid:
            errors = mod.validate_skill(self._path(), {"name": name, "description": "x"})
            assert not any("kebab" in e for e in errors), f"{name} should be valid"
        for name in invalid:
            errors = mod.validate_skill(self._path(), {"name": name, "description": "x"})
            assert any("kebab" in e for e in errors), f"{name} should be invalid"


class TestValidateAgent:
    def _path(self) -> Path:
        return Path("plugins/test/agents/my-agent.md")

    def test_valid_agent(self):
        fields = {"name": "my-agent", "description": "A test agent"}
        errors = mod.validate_agent(self._path(), fields)
        assert errors == []

    def test_valid_with_model(self):
        for model in mod.AGENT_MODELS:
            fields = {"name": "test", "description": "x", "model": model}
            errors = mod.validate_agent(self._path(), fields)
            assert errors == [], f"model '{model}' should be valid"

    def test_invalid_model(self):
        fields = {"name": "test", "description": "x", "model": "gpt-4"}
        errors = mod.validate_agent(self._path(), fields)
        assert any("invalid model" in e for e in errors)

    def test_missing_required_fields(self):
        errors = mod.validate_agent(self._path(), {})
        assert len(errors) == 2

    def test_no_model_is_fine(self):
        fields = {"name": "test", "description": "x"}
        errors = mod.validate_agent(self._path(), fields)
        assert errors == []
