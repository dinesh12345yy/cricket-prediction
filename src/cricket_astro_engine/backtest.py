"""Simple accuracy reporting for pre-generated predictions."""
from __future__ import annotations
import csv
from pathlib import Path

def evaluate_csv(path: str | Path) -> dict:
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("CSV has no data rows")
    required = {"predicted_team", "actual_winner"}
    if not required.issubset(rows[0].keys()):
        raise ValueError(f"CSV must include columns: {', '.join(sorted(required))}")
    valid = [r for r in rows if r.get("predicted_team", "").strip()
             and r.get("actual_winner", "").strip()
             and r["predicted_team"].strip().casefold() not in {"no clear edge", "tie", "unknown"}]
    if not valid:
        raise ValueError("No evaluable predictions in CSV")
    correct = sum(r["predicted_team"].strip().casefold() == r["actual_winner"].strip().casefold() for r in valid)
    return {
        "total_rows": len(rows),
        "evaluable_predictions": len(valid),
        "correct": correct,
        "accuracy_percent": round(correct / len(valid) * 100, 2),
        "warning": "Accuracy alone is insufficient; compare baselines and use a chronological holdout set."
    }
