import os
from pathlib import Path

from cover_letter_cli.export import export_markdown


def test_export_writes_markdown(tmp_path):
    path = tmp_path / "letter.md"
    export_markdown("Dear team,\n\nSincerely,\nDylan", path, inquiry_type="job", tone="professional", model="llama3")

    text = path.read_text(encoding="utf-8")
    assert text.startswith("# Cover Letter")
    assert "Dear team" in text
    assert "Sincerely" in text
    assert "- **Inquiry type:** job" in text
    assert "- **Tone:** professional" in text
    assert "- **Model:** llama3" in text
    assert "## Letter" in text


def test_export_default_path(tmp_path):
    path = tmp_path / "cover-letter-job.md"
    export_markdown("content", path)
    text = path.read_text(encoding="utf-8")
    assert text.startswith("# Cover Letter")
    assert text.strip().endswith("content")
