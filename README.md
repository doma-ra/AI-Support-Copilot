# AI-Support-Copilot (MVP)
![Tests](https://img.shields.io/badge/tests-passing-green)
![tests](https://github.com/doma-ra/AI-Support-Copilot/actions/workflows/pytest.yml/badge.svg)


**Zweck:** Chats/Incidents → **striktes JSON**, **KB-gestützte Antworten**, **aktionsfähige Tickets**.  
**Stack:** Python, pydantic, pytest, Typer.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
python -m eval.evaluator
python cli.py ask "Kartenzahlung fehlgeschlagen"
python cli.py ticket "Rechnung nochmal drucken" --customer "Demo KG"

```

## Features
JSON-Validität (pydantic-Schema, 100 % im MVP)
Router: FAQ-Regeln + KB-Fallback (keine Halluzination)
Tickets: Jira/Zendesk-ähnliche Payload in reports/ticket_payload.json
Eval-Harness: reports/metrics.json mit Raten für JSON, FAQ, KB, Fallback
## Kennzahlen (MVP, Demo-Daten)
json_valid_rate: 1.00
faq_hit_rate: 1.00
kb_hit_rate: 1.00
fallback_rate: 0.00

## Beispiele
python cli.py ask "Kartenzahlung fehlgeschlagen"
python cli.py ask "Internet langsam, bitte Netzwerk prüfen"
python cli.py ticket "Kartenzahlung fehlgeschlagen" --customer "Bar M"
python cli.py ab
### Profile
- Gastro (Default): `python cli.py ask "Kartenzahlung fehlgeschlagen"`
- IT: `KB_PROFILE=it python cli.py ask "VPN verbindet nicht"`

## Nächste Schritte
Prompt v2 mit echtem Provider (per .env) + Repair-Retry
Embedding-Retriever statt Keywords
Mehr Regressionstests und CI (GitHub Actions)
* „A/B-Report zeigt Fallback-Vergleich bei unbekannten Anfragen (reports/ab.csv).“