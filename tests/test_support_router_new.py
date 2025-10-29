from bot.router.support_router import handle_query

def test_handle_query_returns_valid_fields():
    r = handle_query("Kartenzahlung fehlgeschlagen", "gastro")
    assert isinstance(r, dict)
    for key in ("intent", "severity", "answer", "actions", "kb_refs", "escalate"):
        assert key in r
