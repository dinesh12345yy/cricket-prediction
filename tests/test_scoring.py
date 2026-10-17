import json, unittest
from pathlib import Path
from cricket_astro_engine.scoring import score_team, predict_match, load_config
from cricket_astro_engine.tarabala import tara_bala
from cricket_astro_engine.backtest import evaluate_csv

ROOT = Path(__file__).resolve().parents[1]

class EngineTests(unittest.TestCase):
    def setUp(self):
        self.config = load_config(ROOT / "config.json")

    def test_score_is_bounded(self):
        t = score_team({"team":"A","scores":{"dasa":70,"shadbala":70,"ishta":70,"kashta":30,"tarabala":70}}, self.config)
        self.assertGreaterEqual(t.total_score, 0)
        self.assertLessEqual(t.total_score, 100)

    def test_kashta_is_inverted(self):
        low = score_team({"team":"A","scores":{"kashta":10}}, {"weights":{"kashta":1},"score_min":0,"score_max":100})
        high = score_team({"team":"B","scores":{"kashta":90}}, {"weights":{"kashta":1},"score_min":0,"score_max":100})
        self.assertGreater(low.total_score, high.total_score)

    def test_prediction_shape(self):
        match = json.loads((ROOT / "examples/match_input.json").read_text())
        out = predict_match(match, self.config)
        self.assertIn("predicted_team", out)
        self.assertFalse(out["is_calibrated_probability"])

    def test_tarabala(self):
        out = tara_bala("Ashwini", "Bharani")
        self.assertEqual(out["tara_category"], "Sampat")

    def test_backtest(self):
        out = evaluate_csv(ROOT / "examples/historical_results.csv")
        self.assertEqual(out["evaluable_predictions"], 3)
        self.assertAlmostEqual(out["accuracy_percent"], 66.67, places=1)

if __name__ == "__main__":
    unittest.main()
