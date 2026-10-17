from __future__ import annotations
import argparse, json, os
from pathlib import Path
from .scoring import load_config, predict_match
from .backtest import evaluate_csv
from .vedastro_adapter import calculate_dasa_raw
from .tarabala import tara_bala

def main():
    parser = argparse.ArgumentParser(prog="cricket-astro")
    sub = parser.add_subparsers(dest="command", required=True)
    p_score = sub.add_parser("score", help="Score a two-team JSON input")
    p_score.add_argument("input")
    p_score.add_argument("--config", default="config.json")
    p_score.add_argument("--output")
    p_bt = sub.add_parser("backtest", help="Evaluate a CSV of predictions")
    p_bt.add_argument("csv")
    p_tara = sub.add_parser("tarabala", help="Calculate experimental Tara category")
    p_tara.add_argument("--birth-star", required=True)
    p_tara.add_argument("--event-star", required=True)
    p_dasa = sub.add_parser("dasa", help="Fetch raw Dasa periods from VedAstro")
    p_dasa.add_argument("--birth", required=True, help='e.g. "14:30 25/10/1992 +05:30"')
    p_dasa.add_argument("--start", required=True)
    p_dasa.add_argument("--end", required=True)
    p_dasa.add_argument("--location", required=True)
    p_dasa.add_argument("--longitude", required=True, type=float)
    p_dasa.add_argument("--latitude", required=True, type=float)
    p_dasa.add_argument("--output", default="data/dasa_raw.json")
    p_dasa.add_argument("--levels", type=int, default=3)
    p_dasa.add_argument("--precision-hours", type=int, default=24)
    args = parser.parse_args()

    if args.command == "score":
        with open(args.input, encoding="utf-8") as f: match = json.load(f)
        result = predict_match(match, load_config(args.config))
        rendered = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(rendered, encoding="utf-8")
        print(rendered)
    elif args.command == "backtest":
        print(json.dumps(evaluate_csv(args.csv), indent=2))
    elif args.command == "tarabala":
        print(json.dumps(tara_bala(args.birth_star, args.event_star), indent=2, ensure_ascii=False))
    elif args.command == "dasa":
        result = calculate_dasa_raw(args.birth, args.start, args.end, args.location,
            args.longitude, args.latitude, args.output, args.levels,
            args.precision_hours, os.getenv("VEDASTRO_API_KEY"))
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
