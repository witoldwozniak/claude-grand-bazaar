"""Shared test fixtures and helpers."""

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"

# Add scripts/ to sys.path so tests can import script modules directly
sys.path.insert(0, str(SCRIPTS_DIR))
