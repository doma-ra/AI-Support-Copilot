from bot.router.support_router import handle_query

def test_gastro_payment_rule():
    r = handle_query("Kartenzahlung fehlgeschlagen", "gastro")
    assert r["intent"] == "payment"
    assert "Netzwerk" in r["answer"]
    assert r["kb_refs"] == ["faq:PAY-001"]
    assert r["escalate"] is False

def test_it_vpn_rule():
    r = handle_query("VPN verbindet nicht", "it")
    assert r["intent"] == "vpn"
    assert "VPN-Client" in r["answer"]
    assert r["kb_refs"] == ["kb_it:VPN-001"]
    assert r["escalate"] is False
