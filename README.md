# Cricket Astro Engine (experimental)

A modular research prototype combining a VedAstro reference adapter with configurable astrology-style scoring and historical backtesting.

> Important: this is an experimental research tool, not a proven cricket forecasting method. Astrology has not been established as a reliable predictor of match outcomes. Compare it against simple cricket-statistics baselines and report performance honestly.

## Why this is a new engine
- Uses the public `VedAstro/VedAstro.Python` package as a dependency/reference instead of copying its source.
- Keeps match scoring separate from astronomical calculations.
- Stores weights and scoring assumptions in `config.json`.
- Includes an experimental Tarabala helper, CLI scoring, and backtesting.
- Saves raw VedAstro Dasa output for inspection; automatic extraction of active Dasa/Bhukti planets is intentionally not guessed because the API response schema must be verified against a live result.

Reference: https://github.com/VedAstro/VedAstro.Python
VedAstro package: `pip install vedastro`
The referenced Python library is published under the MIT License; this project does not bundle or copy its source.

## Requirements
- Python 3.10+
- Internet access for the VedAstro cloud API adapter
- Optional `vedastro` package only when calling the Dasa API

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
```

Score a sample JSON file:
```bash
cricket-astro score examples/match_input.json --config config.json
```

Run backtesting against a CSV of historical results:
```bash
cricket-astro backtest examples/historical_results.csv
```

The CSV needs `predicted_team`, `actual_winner`, and optionally `match_id`. It measures only predictions you have already generated; do not use the same matches to tune weights and claim an unbiased test.

## VedAstro Dasa lookup

Use a real birth date/time and the relevant local timezone/geo coordinates:
```bash
cricket-astro dasa --birth "14:30 25/10/1992 +05:30" \
  --start "00:00 01/01/2026 +05:30" \
  --end "23:59 31/12/2026 +05:30" \
  --location "Chennai, India" --longitude 80.2707 --latitude 13.0827 \
  --output data/dasa_raw.json
```

This saves the raw response so its exact schema can be inspected before writing a safe parser. Avoid inventing or assuming which Dasa planet is active from unverified output.

## Input model
See `examples/match_input.json`. Each team has a score for each component:
- `dasa`: score for the active Dasa/Bhukti/Antara context, 0–100
- `shadbala`: normalized strength score, 0–100
- `ishta`: Ishta Phala, normalized 0–100
- `kashta`: Kashta Phala, normalized 0–100; higher means more adverse in this project
- `tarabala`: experimental Tara Bala score, 0–100

These are **normalized model inputs**, not raw units from VedAstro. Confirm units and definitions before mapping raw API output to them. The current scoring layer does not automatically calculate all these components.

## Model
For each team:
`score = sum(component_score * configured_weight) / sum(active_weights)`

Higher score is the model's preferred side. The difference is mapped to a heuristic confidence indicator; it is not a calibrated probability.

## Tarabala prototype
The helper uses the conventional 27-nakshatra, 9-Tara cycle from birth nakshatra to event nakshatra. It is a transparent prototype and should be validated with your chosen tradition and source; it is not evidence of sports-prediction ability.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Suggested development sequence
1. Run tests and inspect a sample score.
2. Call Dasa lookup with known test data and save the raw JSON.
3. Confirm the returned schema and the exact Shadbala/Ishta/Kashta API methods in the current VedAstro API reference.
4. Add a tested parser and a reproducible mapping into normalized scores.
5. Keep all match predictions timestamped before the match starts.
6. Compare against majority/home-team and recent-performance baselines on an untouched holdout set.
