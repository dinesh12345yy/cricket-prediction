"""Thin adapter for documented VedAstro Python Dasa API."""
from __future__ import annotations
import json
from pathlib import Path

def calculate_dasa_raw(
    birth_time_text: str,
    start_time_text: str,
    end_time_text: str,
    location_name: str,
    longitude: float,
    latitude: float,
    output_path: str | Path,
    levels: int = 3,
    precision_hours: int = 24,
    api_key: str | None = None,
) -> dict:
    """
    Call the documented Calculate.DasaAtRange API and save raw JSON.
    Exact response parsing is intentionally separate until the real schema is inspected.
    """
    try:
        from vedastro import Calculate, GeoLocation, Time
    except ImportError as exc:
        raise RuntimeError("Install the optional dependency first: pip install '.[vedastro]'") from exc
    if api_key:
        Calculate.SetAPIKey(api_key)
    geo = GeoLocation(location_name, float(longitude), float(latitude))
    birth = Time(birth_time_text, geo)
    start = Time(start_time_text, geo)
    end = Time(end_time_text, geo)
    result = Calculate.DasaAtRange(
        birth, start, end, levels=int(levels), precision_hours=int(precision_hours)
    )
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    return {"output_path": str(output), "result_type": type(result).__name__,
            "top_level_keys": list(result.keys()) if isinstance(result, dict) else None}
