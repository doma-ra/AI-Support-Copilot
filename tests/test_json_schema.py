from bot.schema import BotResponse
def test_schema_example_valid():
    obj = BotResponse(intent="payment", severity="high", answer="OK")
    assert obj.severity == "high"
