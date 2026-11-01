"""Local Markdown export for generated cover letters."""

from __future__ import annotations

from pathlib import Path


def export_markdown(content, path, inquiry_type=None, tone=None, model=None):
    """Write the letter to a Markdown file with a small metadata header."""
    path = Path(path)
    lines = ["# Cover Letter", ""]
    if inquiry_type or tone or model:
        lines.append("## Details")
        lines.append("")
        if inquiry_type:
            lines.append(f"- **Inquiry type:** {inquiry_type}")
        if tone:
            lines.append(f"- **Tone:** {tone}")
        if model:
            lines.append(f"- **Model:** {model}")
        lines.append("")
    lines.append("## Letter")
    lines.append("")
    lines.append(content)
    text = "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")
    return path
