import sys, json
import typer
from pathlib import Path
from bot.schema import BotResponse
from bot.inference import parse_model_output, validate_raw
from bot.router import route_faq
from bot.model import generate_v2
from integrations.ticket_payload import build_ticket

app = typer.Typer(help="AI-Support-Copilot CLI")

@app.command()
def validate(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        raw = f.read()
    ok, result = validate_raw(raw)
    if ok:
        typer.echo(result.model_dump_json(indent=2))
    else:
        typer.echo(result)
        raise typer.Exit(code=1)

@app.command()
def demo():
    example = BotResponse(
        intent="payment",
        severity="high",
        answer="Bitte Terminal neu starten und Verbindung prüfen.",
        actions=["terminal_restart","network_check"],
        kb_refs=["kb/payments/terminal-restart"],
        escalate=False,
        handoff_note=None,
        faq_id="PAY-001",
    )
    typer.echo(example.model_dump_json(indent=2))

@app.command()
def ask(q: str):
    """Erst FAQ/KB-Router. Wenn None: Modell v2 (JSON-garantiert)."""
    res = route_faq(q)
    if res:
        typer.echo(res.model_dump_json(indent=2))
        return
    ok, out = generate_v2(q)
    if ok:
        typer.echo(out.model_dump_json(indent=2))
        return
    raise typer.Exit(code=1)

@app.command()
def ticket(q: str, customer: str = "Demo GmbH", source: str = "chat"):
    """Erzeugt Ticket-Payload und schreibt reports/ticket_payload.json."""
    res = route_faq(q)
    if not res:
        raw = '{"intent":"other","severity":"medium","answer":"Kein FAQ/KB-Treffer","actions":[],"kb_refs":[],"escalate":true,"handoff_note":"Bitte prüfen.","faq_id":null}'
        ok, parsed = validate_raw(raw)
        if not ok:
            raise RuntimeError("Fallback JSON ungültig")
        res = parsed
    payload = build_ticket(res, source=source, customer=customer, query=q)
    out = Path("reports/ticket_payload.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    typer.echo(out.as_posix())

if __name__ == "__main__":
    app()
