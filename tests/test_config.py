import os
from pathlib import Path

from cover_letter_cli.config import (
    AppConfig,
    DEFAULT_CONFIG_PATH,
    DEFAULT_ENDPOINT,
    DEFAULT_MODEL,
    DEFAULT_TONE,
    load_config,
    save_config,
)


def test_load_config_defaults_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "cover_letter_cli.config.DEFAULT_CONFIG_PATH", tmp_path / "config.toml"
    )
    cfg = load_config()
    assert cfg.endpoint == DEFAULT_ENDPOINT
    assert cfg.model == DEFAULT_MODEL
    assert cfg.tone == DEFAULT_TONE


def test_load_config_reads_values(tmp_path, monkeypatch):
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        'endpoint = "http://localhost:9000/v1/chat/completions"\n'
        'model = "mistral"\n'
        'tone = "concise"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr("cover_letter_cli.config.DEFAULT_CONFIG_PATH", config_path)
    cfg = load_config()
    assert cfg.endpoint == "http://localhost:9000/v1/chat/completions"
    assert cfg.model == "mistral"
    assert cfg.tone == "concise"


def test_save_config_writes_toml(tmp_path, monkeypatch):
    config_path = tmp_path / "config.toml"
    monkeypatch.setattr("cover_letter_cli.config.DEFAULT_CONFIG_PATH", config_path)
    cfg = AppConfig(
        endpoint="http://example.com/v1/chat/completions",
        model="llama3",
        tone="warm",
    )
    save_config(cfg)
    text = config_path.read_text(encoding="utf-8")
    assert 'endpoint = "http://example.com/v1/chat/completions"' in text
    assert 'model = "llama3"' in text
    assert 'tone = "warm"' in text
    assert config_path.exists()
