"""Config package for organizer."""

from pathlib import Path

DEFAULT_CONFIG_FILE = Path.home() / ".config" / "organizer" / "config.yaml"

DEFAULT_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
