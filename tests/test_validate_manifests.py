"""Tests for scripts/validate_manifests.py."""

import json
from pathlib import Path

import validate_manifests as mod


def _make_marketplace(tmp_path: Path, data: dict) -> None:
    """Write a marketplace.json file."""
    mp = tmp_path / ".claude-plugin"
    mp.mkdir(parents=True, exist_ok=True)
    (mp / "marketplace.json").write_text(json.dumps(data), encoding="utf-8")


def _make_plugin(tmp_path: Path, name: str, manifest: dict) -> None:
    """Create a plugin directory with plugin.json."""
    plugin_dir = tmp_path / "plugins" / name / ".claude-plugin"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    (plugin_dir / "plugin.json").write_text(json.dumps(manifest), encoding="utf-8")


class TestValidateMarketplace:
    def test_valid_marketplace(self):
        data = {
            "name": "test",
            "owner": {"name": "user"},
            "metadata": {"version": "0.1.0"},
            "plugins": [],
        }
        errors = mod.validate_marketplace(data)
        assert errors == []

    def test_missing_required_fields(self):
        data = {"name": "test"}
        errors = mod.validate_marketplace(data)
        assert len(errors) == 1
        assert "missing required fields" in errors[0]
        assert "metadata" in errors[0]
        assert "owner" in errors[0]
        assert "plugins" in errors[0]

    def test_plugins_not_array(self):
        data = {
            "name": "test",
            "owner": {},
            "metadata": {},
            "plugins": "not-a-list",
        }
        errors = mod.validate_marketplace(data)
        assert any("must be an array" in e for e in errors)

    def test_metadata_not_object(self):
        data = {
            "name": "test",
            "owner": {},
            "metadata": "string",
            "plugins": [],
        }
        errors = mod.validate_marketplace(data)
        assert any("must be an object" in e for e in errors)


class TestValidatePluginEntry:
    def test_valid_plugin(self, tmp_path: Path, monkeypatch: "pytest.MonkeyPatch"):
        monkeypatch.setattr(mod, "PLUGINS_DIR", tmp_path / "plugins")
        _make_plugin(tmp_path, "my-plugin", {
            "name": "my-plugin",
            "version": "1.0.0",
            "description": "A plugin",
            "author": {"name": "user"},
            "license": "MIT",
        })
        entry = {"name": "my-plugin", "source": "my-plugin"}
        errors = mod.validate_plugin_entry(entry, 0)
        assert errors == []

    def test_missing_source_dir(self, tmp_path: Path, monkeypatch: "pytest.MonkeyPatch"):
        monkeypatch.setattr(mod, "PLUGINS_DIR", tmp_path / "plugins")
        (tmp_path / "plugins").mkdir(parents=True)
        entry = {"name": "missing", "source": "missing"}
        errors = mod.validate_plugin_entry(entry, 0)
        assert any("does not exist" in e for e in errors)

    def test_missing_plugin_json(self, tmp_path: Path, monkeypatch: "pytest.MonkeyPatch"):
        monkeypatch.setattr(mod, "PLUGINS_DIR", tmp_path / "plugins")
        (tmp_path / "plugins" / "my-plugin").mkdir(parents=True)
        entry = {"name": "my-plugin", "source": "my-plugin"}
        errors = mod.validate_plugin_entry(entry, 0)
        assert any("missing" in e for e in errors)

    def test_name_mismatch(self, tmp_path: Path, monkeypatch: "pytest.MonkeyPatch"):
        monkeypatch.setattr(mod, "PLUGINS_DIR", tmp_path / "plugins")
        _make_plugin(tmp_path, "my-plugin", {
            "name": "wrong-name",
            "version": "1.0.0",
            "description": "A plugin",
            "author": {"name": "user"},
            "license": "MIT",
        })
        entry = {"name": "my-plugin", "source": "my-plugin"}
        errors = mod.validate_plugin_entry(entry, 0)
        assert any("does not match" in e for e in errors)

    def test_invalid_semver(self, tmp_path: Path, monkeypatch: "pytest.MonkeyPatch"):
        monkeypatch.setattr(mod, "PLUGINS_DIR", tmp_path / "plugins")
        _make_plugin(tmp_path, "my-plugin", {
            "name": "my-plugin",
            "version": "1.0",
            "description": "A plugin",
            "author": {"name": "user"},
            "license": "MIT",
        })
        entry = {"name": "my-plugin", "source": "my-plugin"}
        errors = mod.validate_plugin_entry(entry, 0)
        assert any("not valid semver" in e for e in errors)

    def test_missing_required_fields_in_manifest(
        self, tmp_path: Path, monkeypatch: "pytest.MonkeyPatch"
    ):
        monkeypatch.setattr(mod, "PLUGINS_DIR", tmp_path / "plugins")
        _make_plugin(tmp_path, "my-plugin", {"name": "my-plugin"})
        entry = {"name": "my-plugin", "source": "my-plugin"}
        errors = mod.validate_plugin_entry(entry, 0)
        assert any("missing required fields" in e for e in errors)

    def test_missing_entry_name(self):
        entry = {"source": "my-plugin"}
        errors = mod.validate_plugin_entry(entry, 0)
        assert any("missing 'name'" in e for e in errors)

    def test_missing_entry_source(self):
        entry = {"name": "my-plugin"}
        errors = mod.validate_plugin_entry(entry, 0)
        assert any("missing 'source'" in e for e in errors)
