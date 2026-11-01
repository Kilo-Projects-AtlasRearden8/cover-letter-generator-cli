# cover-letter-cli

Local-first CLI for writing cover letters — job applications and reselling
inquiries — through any OpenAI-compatible endpoint, with **Ollama as the
default** so no API keys are ever needed. Letters are exported to local
Markdown files.

Built by [Asdale Dynamics, LLC](https://dylanasdale.github.io) (Indiana, formed
October 2026), founded by Dylan Asdale, a registered nurse turned AI author of
*The Massive AI Manual*. Asdale Dynamics publishes beginner-friendly AI
education, books, guides, and practical open-source tools — written plain
English, step by step, never condescending, like a friend would explain it.

## What it does

- Generates cover letters for **job** applications and **reselling**
  inquiries (wholesale, dropshipping, listing partnerships, etc.)
- Lets you pick a **tone**: professional, warm, enthusiastic, concise,
  confident, or friendly
- Talks to any OpenAI-compatible `/v1/chat/completions` endpoint; defaults to
  `http://localhost:11434/v1/chat/completions` (Ollama)
- Exports each letter to a local Markdown file with a small metadata header
- No secrets, no API keys, no personal data stored by the tool

## Install

```bash
pip install cover-letter-cli
```

Or run from source:

```bash
pip install -e .
cover-letter --help
```

## Usage

Create a default config (stored at `~/.cover-letter-cli/config.toml`):

```bash
cover-letter init-config
```

Write a job cover letter:

```bash
cover-letter write --type job --tone professional \
  --recipient "Hiring Manager" \
  --company "Acme Home Health" \
  --position "Registered Nurse" \
  --sender "Dylan Asdale" \
  --key-points "5 years med-surg experience" \
  --key-points "Committed to patient education"
```

Write a reselling inquiry:

```bash
cover-letter write --type reselling --tone warm \
  --recipient "Buying Team" \
  --company "Bronze Goods Wholesale" \
  --position "Wholesale partnership inquiry" \
  --sender "Dylan Asdale" \
  --output my-inquiry.md
```

Use a different endpoint (e.g. another OpenAI-compatible server):

```bash
cover-letter --endpoint http://localhost:8080/v1/chat/completions --model mistral write ...
```

Show effective configuration:

```bash
cover-letter config
```

Preview the prompt without calling the endpoint:

```bash
cover-letter write --type job --dry-run ...
```

## Testing

Tests use a mocked HTTP endpoint — no network, no keys:

```bash
pytest
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## Credit

Created by Asdale Dynamics, LLC — beginner-friendly AI education, books, and
practical tools from Dylan Asdale. Learn more at dylanasdale.github.io.
