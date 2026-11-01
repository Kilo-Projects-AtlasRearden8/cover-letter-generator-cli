# cover-letter-cli

A local-first command-line tool that writes cover letters for job applications
and reselling inquiries — using any OpenAI-compatible endpoint, with Ollama as
the default so you never need an API key.

Built by [Asdale Dynamics, LLC](https://dylanasdale.github.io) (Indiana, formed
October 2026), founded by Dylan Asdale, a registered nurse turned AI author of
*The Massive AI Manual*. Like everything Asdale Dynamics puts out, this tool is
written to be clear, warm, and beginner-friendly — explained like a friend
would explain it, step by step, never condescending.

## What it does

- Writes cover letters for **job** applications (for example, nursing,
  healthcare, or any other role)
- Writes cover letters for **reselling** inquiries (for example reaching out to
  wholesalers for an eBay or Amazon reselling business)
- Lets you pick a **tone**: professional, warm, enthusiastic, concise,
  confident, or friendly
- Talks to any OpenAI-compatible chat endpoint; defaults to local Ollama
  (`http://localhost:11434/v1/chat/completions`)
- Saves each letter as a local Markdown file — nothing leaves your machine
  unless you choose to send it to your own endpoint
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

You'll need Python 3.11 or newer.

## First-time setup

Create a default config file (stored at `~/.cover-letter-cli/config.toml`):

```bash
cover-letter init-config
```

This writes a config that points at your local Ollama endpoint with the
`llama3` model. If you don't have Ollama running yet, install it from
https://ollama.com and pull a model:

```bash
ollama pull llama3
```

Then check your effective configuration:

```bash
cover-letter config
```

You should see:

```
endpoint: http://localhost:11434/v1/chat/completions
model: llama3
tone: professional
```

## Write a cover letter

### Job application

```bash
cover-letter write --type job --tone professional \
  --recipient "Hiring Manager" \
  --company "Acme Home Health" \
  --position "Registered Nurse" \
  --sender "Dylan Asdale" \
  --key-points "5 years med-surg experience" \
  --key-points "Committed to patient education"
```

This creates `cover-letter-job.md` in your current folder.

### Reselling inquiry (eBay / Amazon / wholesale)

```bash
cover-letter write --type reselling --tone warm \
  --recipient "Buying Team" \
  --company "Bronze Goods Wholesale" \
  --position "Wholesale partnership inquiry" \
  --sender "Dylan Asdale" \
  --key-points "eBay and Amazon seller" \
  --key-points "Looking for wholesale inventory" \
  --output my-inquiry.md
```

This creates `my-inquiry.md`.

### Pick a tone

Choose from: `professional`, `warm`, `enthusiastic`, `concise`, `confident`,
`friendly`. The tone changes how the letter is written, not just a label.

### Use a different endpoint

If you run another OpenAI-compatible server (for example a different local LLM):

```bash
cover-letter --endpoint http://localhost:8080/v1/chat/completions --model mistral write ...
```

### Preview without calling the endpoint

Use `--dry-run` to print the prompt that would be sent, without contacting the
LLM at all:

```bash
cover-letter write --type job --tone professional --dry-run ...
```

## Testing

Tests use a mocked HTTP endpoint — no network, no API keys:

```bash
pytest
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## Credit

Created by Asdale Dynamics, LLC — beginner-friendly AI education, books, and
practical tools from Dylan Asdale. Learn more at dylanasdale.github.io.
