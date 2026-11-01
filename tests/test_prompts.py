from cover_letter_cli.prompts import TONES, build_messages


def test_build_messages_contains_details():
    messages = build_messages(
        "job", "professional", "Hiring Manager", "Acme Co", "Nurse", "Dylan",
        ["skilled", "kind"],
    )
    assert messages[0]["role"] == "system"
    user = messages[1]["content"]
    assert "Hiring Manager" in user
    assert "Acme Co" in user
    assert "Nurse" in user
    assert "Dylan" in user
    assert "skilled" in user
    assert "kind" in user


def test_build_messages_reselling_type():
    messages = build_messages(
        "reselling", "warm", "Buyer", "Bronze Goods", "Wholesale inquiry", "Dylan",
        ["eBay seller"],
    )
    user = messages[1]["content"]
    assert "reselling" in user.lower()
    assert "eBay seller" in user


def test_build_messages_tone_reflected():
    base = build_messages("job", "professional", "R", "C", "P", "S", [])
    enthusiastic = build_messages("job", "enthusiastic", "R", "C", "P", "S", [])
    assert base[1]["content"] != enthusiastic[1]["content"]
    assert "professional" in base[1]["content"]
    assert "enthusiastic" in enthusiastic[1]["content"]


def test_unknown_tone_raises():
    import pytest
    with pytest.raises(ValueError):
        build_messages("job", "not-a-tone", "R", "C", "P", "S", [])


def test_unknown_type_raises():
    import pytest
    with pytest.raises(ValueError):
        build_messages("not-a-type", "professional", "R", "C", "P", "S", [])


def test_tones_nonempty():
    assert "professional" in TONES
    assert all(isinstance(desc, str) and desc for desc in TONES.values())
