"""Configuration loading for the cover letter CLI.

Configuration lives in a TOML file (default: ~/.cover-letter-cli/config.toml).
All values have sensible defaults so the tool works out of the box with a
local Ollama endpoint and no API keys.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib

DEFAULT_ENDPOINT = "http://localhost:11434/v1/chat/completions"
DEFAULT_MODEL = "llama3"
DEFAULT_TONE = "professional"
DEFAULT_CONFIG_PATH = Path.home() / ".cover-letter-cli" / "config.toml"


@dataclass
class AppConfig:
    endpoint: str = DEFAULT_ENDPOINT
    model: str = DEFAULT_MODEL
    tone: str = DEFAULT_TONE


def load_config(path: str | Path | None = None) -> AppConfig:
    """Load configuration, falling back to defaults for missing values."""
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    config = AppConfig()
    if config_path.exists():
        with open(config_path, "rb") as handle:
            data = tomllib.load(handle)
        config.endpoint = data.get("endpoint", config.endpoint)
        config.model = data.get("model", config.model)
        config.tone = data.get("tone", config.tone)
    return config


def save_config(config: AppConfig, path: str | Path | None = None) -> None:
    """Persist configuration to the default config path."""
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    config_path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        f'endpoint = "{config.endpoint}"\n'
        f'model = "{config.model}"\n'
        f'tone = "{config.tone}"\n'
    )
    config_path.write_text(text, encoding="utf-8")
