import json
import os
import shutil
import tempfile
import unittest

from _load import load, example

plan = load("gruender-plan", "compile")


class Compile(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        with open(os.path.join(self.d, "idee.md"), "w", encoding="utf-8") as fh:
            fh.write("# Moss Matcha Bar\n\nEin Matcha-Café zum Mitnehmen in der Sendlinger Straße.\n")

    def tearDown(self):
        shutil.rmtree(self.d)

    def numbers(self, **change):
        with open(example("gruender-finanzen", "example.json"), encoding="utf-8") as fh:
            s = json.load(fh)
        s.update(change)
        with open(os.path.join(self.d, "zahlen.json"), "w") as fh:
            json.dump(s, fh)

    def panel(self, buys, n=100):
        os.makedirs(os.path.join(self.d, "panel"), exist_ok=True)
        with open(os.path.join(self.d, "panel", "ergebnis.json"), "w") as fh:
            json.dump({"buys": buys, "passes": n - buys, "answered": n, "buy_rate": buys / float(n)}, fh)

    def test_no_numbers_is_incomplete(self):
        v, text = plan.compile_plan(self.d)
        self.assertEqual(v, "Unvollständig")
        self.assertIn("starte /gruender-finanzen", text)

    def test_good_numbers_and_panel_is_profitable(self):
        self.numbers()
        self.panel(40)
        v, text = plan.compile_plan(self.d)
        self.assertEqual(v, "Profitabel")
        self.assertTrue(text.startswith("# Moss Matcha Bar · Businessplan"))
        self.assertIn("| Gewinnmarge beim Plan | 38% je Tasse |", text)
        self.assertIn("40 kaufen · 60 lehnen ab", text)
        self.assertIn("- Das Käuferpanel: starte /gruender-kunden", text.replace("## Noch offen", ""))

    def test_a_weak_panel_means_not_yet(self):
        self.numbers()
        self.panel(12)
        v, text = plan.compile_plan(self.d)
        self.assertEqual(v, "Noch nicht")
        self.assertIn("✗ 12 von 100 simulierten Käufern kaufen", text)

    def test_losing_money_means_not_yet(self):
        self.numbers(price=3.00)
        v, _ = plan.compile_plan(self.d)
        self.assertEqual(v, "Noch nicht")


if __name__ == "__main__":
    unittest.main()
