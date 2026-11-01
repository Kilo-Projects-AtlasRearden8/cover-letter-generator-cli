# STATUS

## What was built

`cover-letter-cli` — a local-first Python CLI that writes cover letters for job
applications and reselling inquiries (wholesale, dropshipping, listing
partnerships, etc.) through any OpenAI-compatible chat completions endpoint.
Ollama (`http://localhost:11434/v1/chat/completions`) is the default, so no API
keys or secrets are required. Users pick a tone (professional, warm,
enthusiastic, concise, confident, friendly) and each generated letter is
exported to a local Markdown file with a metadata header.

Built for Asdale Dynamics, LLC (Indiana, formed Oct 2026) — Dylan Asdale's
beginner-friendly AI education and tools project. Plain English, tested,
local-first.

## Contents

- `pyproject.toml` — package metadata, `cover-letter` console script, deps: click, httpx
- `cover_letter_cli/cli.py` — Click CLI (`write`, `config`, `init-config`)
- `cover_letter_cli/client.py` — OpenAI-compatible endpoint client with clear errors
- `cover_letter_cli/prompts.py` — tone-aware prompt templates
- `cover_letter_cli/export.py` — local Markdown export
- `cover_letter_cli/config.py` — TOML config at `~/.cover-letter-cli/config.toml`
- `tests/` — 16 tests, all mocked via `httpx.MockTransport` (no network, no keys)
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `README.md` — usage docs, credits Asdale Dynamics, LLC
- `.gitignore`

## How to run

```bash
pip install -e .              # or: pip install cover-letter-cli
cover-letter init-config      # writes default config
cover-letter config           # show endpoint/model/tone
cover-letter write --type job --tone professional \
  --recipient "Hiring Manager" --company "Acme Co" \
  --position "Nurse" --sender "Dylan" \
  --key-points "skilled" --output letter.md
cover-letter write --type reselling --tone warm ...
cover-letter write --dry-run ...   # preview prompt, no endpoint call
cover-letter --endpoint http://localhost:8080/v1/chat/completions write ...
```

Tests:

```bash
pytest            # 16 passed, fully mocked endpoints
```

## Verification results

- `python3 -m pytest -q`: 16 passed (client request/response handling, errors, prompts, export, CLI write/dry-run/config)
- `pip install -e .` in isolated venv: OK
- `cover-letter --help`: OK
- `cover-letter write --dry-run`: OK (no endpoint required)
- `cover-letter config`: OK
- Git: initialized, one commit on `master`, no remote, nothing pushed
- No `.github/workflows`, no secrets or personal data in any file

## Known gaps

- Generating a real letter requires a running OpenAI-compatible endpoint (Ollama default); unreachable endpoints fail with a clear message.
- Default model `llama3` must be pulled in Ollama first (`ollama pull llama3`) or overridden with `--model`.
- Authentication is intentionally unsupported (no keys by design).
- Config file is not created automatically; run `cover-letter init-config` or pass `--config`.
- Reselling inquiry fields are generic (recipient/company/position/sender); no platform-specific eBay/Amazon templates yet.
