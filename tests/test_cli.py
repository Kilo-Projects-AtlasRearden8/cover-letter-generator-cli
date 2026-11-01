from click.testing import CliRunner

from cover_letter_cli.cli import cli


class FakeClient:
    def __init__(self, endpoint, model, transport=None, timeout=60.0):
        self.endpoint = endpoint
        self.model = model

    def generate(self, messages):
        return "Dear Hiring Manager,\n\nI am excited.\n\nSincerely,\nDylan"

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()


def test_cli_write_creates_markdown(tmp_path, monkeypatch):
    import cover_letter_cli.cli as cli_module

    monkeypatch.setattr(cli_module, "LLMClient", FakeClient)

    runner = CliRunner()
    output_path = str(tmp_path / "my-letter.md")
    result = runner.invoke(
        cli,
        [
            "write",
            "--type", "job",
            "--tone", "professional",
            "--recipient", "Hiring Manager",
            "--company", "Acme Co",
            "--position", "Nurse",
            "--sender", "Dylan",
            "--key-points", "skilled",
            "--output", output_path,
        ],
        standalone_mode=False,
    )

    assert result.exit_code == 0, result.output
    path = tmp_path / "my-letter.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Dear Hiring Manager" in text
    assert "- **Inquiry type:** job" in text


def test_cli_write_reselling(tmp_path, monkeypatch):
    import cover_letter_cli.cli as cli_module

    monkeypatch.setattr(cli_module, "LLMClient", FakeClient)

    runner = CliRunner()
    output_path = str(tmp_path / "reselling.md")
    result = runner.invoke(
        cli,
        [
            "write",
            "--type", "reselling",
            "--tone", "warm",
            "--recipient", "Buyer",
            "--company", "Bronze Goods",
            "--position", "Wholesale",
            "--sender", "Dylan",
            "--output", output_path,
        ],
        standalone_mode=False,
    )

    assert result.exit_code == 0, result.output
    path = tmp_path / "reselling.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "- **Tone:** warm" in text


def test_cli_dry_run_prints_prompt(monkeypatch):
    import cover_letter_cli.cli as cli_module

    calls = []

    class NoCallClient:
        def generate(self, messages):
            calls.append(messages)
            return "should not be called"

    monkeypatch.setattr(cli_module, "LLMClient", NoCallClient)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "write",
            "--type", "reselling",
            "--tone", "warm",
            "--recipient", "Buyer",
            "--company", "Bronze Goods",
            "--position", "Wholesale",
            "--sender", "Dylan",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "--- Prompt (dry run" in result.output
    assert "Wholesale" in result.output
    assert calls == []


def test_cli_config_show():
    runner = CliRunner()
    result = runner.invoke(cli, ["config"])
    assert result.exit_code == 0, result.output
    assert "endpoint:" in result.output
    assert "model:" in result.output
    assert "tone:" in result.output
