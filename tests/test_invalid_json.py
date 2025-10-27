from bot.inference import validate_raw

def test_invalid_json_is_caught():
    ok, msg = validate_raw("not json at all")
    assert ok is False
    assert "JSONDecodeError" in msg

def test_schema_violation_is_caught():
    # severity ist absichtlich ungültig
    raw = '{"intent":"payment","severity":"ultra","answer":"x"}'
    ok, msg = validate_raw(raw)
    assert ok is False
    assert "ValidationError" in msg
    assert "severity" in msg
