from bot.router import route_faq

def test_route_payment_hit():
    res = route_faq("Kartenzahlung fehlgeschlagen seit 05:12 Uhr")
    assert res is not None
    assert res.faq_id == "PAY-001"
    assert res.escalate is False

def test_route_receipt_hit():
    res = route_faq("Bitte Rechnung nochmal drucken")
    assert res is not None
    assert res.faq_id == "REC-001"
