import typer
from bot.schema import BotResponse
from bot.inference import parse_model_output

app = typer.Typer(help="AI-Support-Copilot CLI")

@app.command()
def validate(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        raw = f.read()
    model = parse_model_output(raw)
    typer.echo(model.model_dump_json(indent=2))

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

if __name__ == "__main__":
    app()
