from pathlib import Path


def test_skill_exists_and_contains_non_negotiables():
    root = Path(__file__).resolve().parents[1]
    skill = root / "skills" / "damaged-qr-recovery" / "SKILL.md"
    assert skill.exists()
    text = skill.read_text(encoding="utf-8")
    assert "Reed-Solomon" in text
    assert "Do not fabricate" in text
    assert "visible source module" in text
    assert "AMBIGUOUS" in text
