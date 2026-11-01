"""Command line interface for the cover letter generator."""

from __future__ import annotations

from pathlib import Path

import click

from .client import LLMClient, LLMError
from .config import DEFAULT_CONFIG_PATH, AppConfig, load_config, save_config
from .export import export_markdown
from .prompts import TONES, build_messages

INQUIRY_TYPES = ["job", "reselling"]


@click.group()
@click.option(
    "--endpoint",
    envvar="COVER_LETTER_ENDPOINT",
    default=None,
    help="OpenAI-compatible chat completions URL (default: local Ollama).",
)
@click.option("--model", envvar="COVER_LETTER_MODEL", default=None, help="Model name.")
@click.option(
    "--config",
    type=click.Path(dir_okay=False),
    default=None,
    help=f"Config TOML path (default: {DEFAULT_CONFIG_PATH}).",
)
@click.pass_context
def cli(ctx, endpoint, model, config):
    """cover-letter: write cover letters with local LLMs, no API keys required."""
    cfg = load_config(config)
    if endpoint:
        cfg.endpoint = endpoint
    if model:
        cfg.model = model
    ctx.obj = cfg


@cli.command("config")
@click.pass_obj
def config_show(cfg):
    """Show the effective configuration."""
    click.echo(f"endpoint: {cfg.endpoint}")
    click.echo(f"model: {cfg.model}")
    click.echo(f"tone: {cfg.tone}")


@cli.command("init-config")
@click.pass_obj
def init_config(cfg):
    """Write a default config file to the standard location."""
    save_config(cfg)
    click.echo(f"Wrote default config to {DEFAULT_CONFIG_PATH}")


@cli.command()
@click.option(
    "--type",
    "inquiry_type",
    type=click.Choice(INQUIRY_TYPES),
    required=True,
    help="Type of inquiry: job or reselling.",
)
@click.option(
    "--tone",
    type=click.Choice(sorted(TONES)),
    default="professional",
    show_default=True,
    help="Tone of the letter.",
)
@click.option("--recipient", required=True, help="Person or team the letter is addressed to.")
@click.option("--company", required=True, help="Company the letter is addressed to.")
@click.option(
    "--position",
    required=True,
    help="Job role (job inquiries) or inquiry subject (reselling inquiries).",
)
@click.option("--sender", required=True, help="Name to sign the letter with.")
@click.option(
    "--key-points",
    multiple=True,
    help="Key points to include (repeat for more than one).",
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False),
    default=None,
    help="Output Markdown path (default: cover-letter-<type>.md).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Print the prompt instead of calling the LLM endpoint.",
)
@click.pass_obj
def write(cfg, inquiry_type, tone, recipient, company, position, sender, key_points, output, dry_run):
    """Generate a cover letter and export it to Markdown."""
    messages = build_messages(
        inquiry_type, tone, recipient, company, position, sender, list(key_points)
    )

    if dry_run:
        click.echo("--- Prompt (dry run, no endpoint call) ---")
        for message in messages:
            click.echo(f"[{message['role']}] {message['content']}")
        return

    default_output = f"cover-letter-{inquiry_type}.md"
    output_path = Path(output) if output else Path(default_output)

    with LLMClient(cfg.endpoint, cfg.model) as client:
        try:
            content = client.generate(messages)
        except LLMError as exc:
            raise click.ClickException(str(exc))

    export_markdown(
        content,
        output_path,
        inquiry_type=inquiry_type,
        tone=tone,
        model=cfg.model,
    )
    click.echo(f"Wrote {output_path}")
