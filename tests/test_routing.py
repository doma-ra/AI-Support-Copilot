from bot.router import route_faq
def test_route_returns_none_now():
    assert route_faq("Kartenzahlung fehlgeschlagen") is None
