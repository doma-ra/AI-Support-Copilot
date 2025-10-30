# AI-Support-Copilot (MVP)
![Tests](https://img.shields.io/badge/tests-passing-green)
![tests](https://github.com/doma-ra/AI-Support-Copilot/actions/workflows/pytest.yml/badge.svg)

**Zweck:** Chats/Incidents → **striktes JSON**, **KB-gestützte Antworten**, **aktionsfähige Tickets**.  
**Stack:** Python, Pydantic, Pytest, Typer.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r [requirements.txt](http://_vscodecontentref_/1)
python -m pytest -q
python -m eval.evaluator
python [cli.py](http://_vscodecontentref_/2) ask "Kartenzahlung fehlgeschlagen"
python [cli.py](http://_vscodecontentref_/3) ticket "Rechnung nochmal drucken" --customer "Demo KG"
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

## allO AI Support Agent Prototype

Zweck: Demonstration eines testbaren AI-Support-Backends für Gastronomie und IT mit stabilen JSON-Antworten, Logging und automatisierten Tests.

### Start
```bash
python -m uvicorn api.main:app --reload
# oder alternativer Port
python -m uvicorn api.main:app --reload --port 8001
```

### Beispiele (HTTP)

# Gastro
curl -s -X POST http://127.0.0.1:8001/ask -H "content-type: application/json" \
  -d '{"query":"Kartenzahlung fehlgeschlagen","profile":"gastro"}'

# IT
curl -s -X POST http://127.0.0.1:8001/ask -H "content-type: application/json" \
  -d '{"query":"VPN verbindet nicht","profile":"it"}'

# Ticket anlegen
curl -s -X POST http://127.0.0.1:8001/ticket -H "content-type: application/json" \
  -d '{"title":"Bondrucker druckt nicht","description":"Seit 12:10 kein Bon","profile":"gastro","priority":"high"}'

### CLI

python cli.py ask "Kartenzahlung fehlgeschlagen" --profile gastro

### Health/Version

curl -s http://127.0.0.1:8001/health
curl -s http://127.0.0.1:8001/version

### Provider Switch

# Standard (lokal)
export PROVIDER=mock
# später für echten Adapter:
export PROVIDER=openai

### Logs und Artefakte
Requests: logs/requests.jsonl
Ticket-Payloads: reports/ticket_payload.json

### Tests

pytest -q

## Demo & Deployment

### Lokaler Start
bash
# API starten
python -m uvicorn api.main:app --reload --port 8001

### Beispielaufrufe
```bash
curl -s -X POST http://127.0.0.1:8001/ask \
  -H "content-type: application/json" \
  -d '{"query":"Kartenzahlung fehlgeschlagen","profile":"gastro"}'

curl -s -X POST http://127.0.0.1:8001/ticket \
  -H "content-type: application/json" \
  -d '{"title":"Bondrucker defekt","description":"Kein Druck seit 14:10","profile":"gastro"}'
```
