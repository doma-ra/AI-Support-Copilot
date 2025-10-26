import json
from pydantic import ValidationError
from .schema import BotResponse

def parse_model_output(raw: str) -> BotResponse:
    """Parst Roh-String strikt ins Schema. Wirft Exceptions bei Fehlern."""
    data = json.loads(raw)
    return BotResponse.model_validate(data)

def validate_raw(raw: str):
    """
    Liefert (ok, result).
    ok=True  -> result ist BotResponse.
    ok=False -> result ist ein Fehlertext (str).
    """
    try:
        model = parse_model_output(raw)
        return True, model
    except json.JSONDecodeError as e:
        return False, f"JSONDecodeError: {e.msg} at pos {e.pos}"
    except ValidationError as e:
        return False, f"ValidationError: {e.errors()}"
