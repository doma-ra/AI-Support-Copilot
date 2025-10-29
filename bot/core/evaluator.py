import json, time, os, csv
from bot.router.support_router import handle_query
from bot.schemas.response import BotResponse

SCENARIOS = [
    ("gastro", "Kartenzahlung fehlgeschlagen"),
    ("gastro", "Bondrucker druckt nicht"),
    ("it", "VPN verbindet nicht"),
    ("it", "SSO Login geht nicht"),
]

def run():
    os.makedirs("reports", exist_ok=True)
    rows, latencies = [], []
    valid_count = 0

    for profile, query in SCENARIOS:
        t0 = time.time()
        resp = handle_query(query, profile)
        dt = round((time.time() - t0) * 1000, 2)
        latencies.append(dt)
        try:
            BotResponse(**resp)  # Validierung
            valid = 1
        except Exception:
            valid = 0
        valid_count += valid
        rows.append({"profile": profile, "query": query, "ms": dt, "valid": valid, "intent": resp.get("intent","")})

    # CSV
    with open("reports/ab.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["profile","query","ms","valid","intent"])
        w.writeheader(); w.writerows(rows)

    # Metrics JSON
    metrics = {
        "total": len(rows),
        "json_valid_rate": round(valid_count / max(1, len(rows)), 2),
        "p50_ms": percentile(latencies, 50),
        "p95_ms": percentile(latencies, 95),
    }
    with open("reports/metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

def percentile(values, p):
    if not values: return 0.0
    s = sorted(values)
    k = (len(s)-1) * (p/100)
    f = int(k); c = min(f+1, len(s)-1)
    return round(s[f] + (s[c]-s[f])*(k-f), 2)

if __name__ == "__main__":
    run()
