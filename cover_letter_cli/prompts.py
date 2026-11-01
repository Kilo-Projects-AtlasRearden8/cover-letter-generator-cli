"""Prompt templates for cover letters.

Tones are written plain-English and beginner friendly, matching the Asdale
Dynamics voice: warm, clear, never condescending.
"""

from __future__ import annotations

TONES: dict[str, str] = {
    "professional": "polished and business-appropriate",
    "warm": "friendly and personable",
    "enthusiastic": "energetic and eager",
    "concise": "short and to the point",
    "confident": "self-assured and direct",
    "friendly": "approachable and kind",
}

TONE_DESCRIPTIONS = "\n".join(f"  - {name}: {desc}" for name, desc in TONES.items())

SYSTEM_PROMPT = (
    "You are a helpful writing assistant. Write a cover letter based on the "
    "details provided. Use the requested tone. Output only the letter, in "
    "Markdown, with no extra commentary."
)


def _job_user_prompt(tone, recipient, company, position, sender, key_points):
    points = "\n".join(f"- {point}" for point in key_points) if key_points else "- (none provided)"
    return (
        f"Write a cover letter for a job application.\n"
        f"Recipient: {recipient}\n"
        f"Company: {company}\n"
        f"Position: {position}\n"
        f"Sender: {sender}\n"
        f"Tone: {tone}\n"
        f"Key points to include:\n{points}\n"
        f"Address the letter to {recipient} at {company} for the {position} role. "
        f"Sign it as {sender}."
    )


def _reselling_user_prompt(tone, recipient, company, position, sender, key_points):
    points = "\n".join(f"- {point}" for point in key_points) if key_points else "- (none provided)"
    return (
        f"Write a cover letter for a reselling business inquiry.\n"
        f"Recipient: {recipient}\n"
        f"Company: {company}\n"
        f"Subject / role: {position}\n"
        f"Sender: {sender}\n"
        f"Tone: {tone}\n"
        f"Key points to include:\n{points}\n"
        f"Address the letter to {recipient} at {company}. The sender, {sender}, "
        f"is inquiring about reselling opportunities (for example wholesale, "
        f"dropshipping, or listing partnerships). Sign it as {sender}."
    )


def build_messages(inquiry_type, tone, recipient, company, position, sender, key_points):
    """Build the chat messages for the LLM endpoint."""
    if tone not in TONES:
        raise ValueError(f"Unknown tone '{tone}'. Choose from: {', '.join(TONES)}")

    if inquiry_type == "job":
        user = _job_user_prompt(tone, recipient, company, position, sender, key_points)
    elif inquiry_type == "reselling":
        user = _reselling_user_prompt(tone, recipient, company, position, sender, key_points)
    else:
        raise ValueError(f"Unknown inquiry type '{inquiry_type}'. Choose 'job' or 'reselling'.")

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]
