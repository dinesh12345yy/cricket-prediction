"""Configurable scoring logic. Inputs must already be normalized to 0..100."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
import json
from pathlib import Path

COMPONENTS = ("dasa", "shadbala", "ishta", "kashta", "tarabala")

@dataclass
class TeamScore:
    team: str
    total_score: float
    components: dict[str, float | None]
    explanation: str

def load_config(path: str | Path = "config.json") -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    weights = config.get("weights", {})
    if not weights or any(k not in COMPONENTS for k in weights):
        raise ValueError("config.weights must contain known component names")
    if any(float(v) < 0 for v in weights.values()):
        raise ValueError("Weights must be non-negative")
    if sum(float(v) for v in weights.values()) <= 0:
        raise ValueError("At least one weight must be positive")
    return config

def score_team(team_data: dict[str, Any], config: dict[str, Any]) -> TeamScore:
    name = str(team_data.get("team", "Unknown"))
    weights = config["weights"]
    min_score = float(config.get("score_min", 0))
    max_score = float(config.get("score_max", 100))
    weighted_sum = 0.0
    active_weight = 0.0
    used: dict[str, float | None] = {}
    for component in COMPONENTS:
        raw = team_data.get("scores", {}).get(component)
        if raw is None or component not in weights or float(weights[component]) == 0:
            used[component] = None
            continue
        value = float(raw)
        if not min_score <= value <= max_score:
            raise ValueError(f"{name}.{component} must be between {min_score} and {max_score}")
        weight = float(weights[component])
        # Kashta is supplied as a positive adversity score; invert it before combining.
        effective = max_score - value if component == "kashta" else value
        weighted_sum += effective * weight
        active_weight += weight
        used[component] = value
    if active_weight == 0:
        raise ValueError(f"No usable weighted scores supplied for {name}")
    total = weighted_sum / active_weight
    return TeamScore(name, round(total, 3), used,
                     "Kashta is inverted; missing components are excluded and weights renormalized.")

def predict_match(match: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    teams = match.get("teams", [])
    if len(teams) != 2:
        raise ValueError("Input must contain exactly two teams")
    a, b = (score_team(t, config) for t in teams)
    delta = round(a.total_score - b.total_score, 3)
    if abs(delta) < 0.001:
        predicted = "No clear edge"
    else:
        predicted = a.team if delta > 0 else b.team
    scale = float(config.get("confidence_scale", 2.0))
    # Heuristic indicator only, deliberately not called a probability.
    indicator = round(100 / (1 + pow(2.718281828, -abs(delta) / max(scale, 0.001))), 1)
    return {
        "match_id": match.get("match_id", "unspecified"),
        "predicted_team": predicted,
        "score_difference_team_a_minus_team_b": delta,
        "heuristic_edge_indicator_percent": indicator,
        "is_calibrated_probability": False,
        "team_scores": [asdict(a), asdict(b)],
        "warning": "Experimental astrology-based scoring; not a validated or reliable sports forecast."
    }
