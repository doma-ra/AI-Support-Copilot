from bot.schemas.ticket import Ticket

def test_ticket_valid_minimal():
    t = Ticket(title="SSO Login geht nicht", description="Fehler nach MFA", profile="it")
    assert t.priority == "medium"
    assert t.profile == "it"

def test_ticket_rejects_short_title():
    import pytest
    with pytest.raises(Exception):
        Ticket(title="x", description="y")
