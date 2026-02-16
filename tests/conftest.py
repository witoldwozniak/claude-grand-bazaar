"""Shared test fixtures and helpers."""

import importlib.util
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"

# Add scripts/ to sys.path for underscore-named modules
sys.path.insert(0, str(SCRIPTS_DIR))


def _import_script(name: str, filename: str):
    """Import a script that has a hyphenated filename (not a valid Python identifier)."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# Pre-import hyphenated scripts so tests can use `import index_research as mod`
_import_script("index_research", "index-research.py")
_import_script("index_decisions", "index-decisions.py")
