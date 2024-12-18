import unittest
import numpy as np

class TestUtopischScenario(unittest.TestCase):
    def setUp(self):
        # Dataset en parameters zoals in de hoofdcode
        self.data_utopisch = {
            "Douche": {"mean": 50, "reduction_rate": 0.30},
            "Toilet": {"mean": 35, "reduction_rate": 0.40},
            "Overig": {"mean": 24.5, "reduction_rate": 0.10},
        }
        self.n_simulations = 10000
        self.future_years = 10

    def test_simulation_output(self):
        simulated_totals_utopisch = []
        for year in range(self.future_years):
            yearly_total = sum(
                np.mean(np.random.normal(
                    stats["mean"] * (1 - stats["reduction_rate"] * year / self.future_years),
                    stats["mean"] * 0.1,
                    self.n_simulations
                ))
                for stats in self.data_utopisch.values()
            )
            simulated_totals_utopisch.append(yearly_total)

        # Test: Output moet een lijst zijn
        self.assertIsInstance(simulated_totals_utopisch, list, "Output is not a list.")

        # Test: Geen negatieve waarden in de output
        for value in simulated_totals_utopisch:
            self.assertGreaterEqual(value, 0, "Watergebruik kan niet negatief zijn.")

        # Test: Outputlengte moet gelijk zijn aan future_years
        self.assertEqual(len(simulated_totals_utopisch), self.future_years,
                         "Outputlengte komt niet overeen met het aantal voorspelde jaren.")

        # Test: Consistente reductietrend (latere jaren moeten minder watergebruik hebben dan eerdere jaren)
        self.assertTrue(
            all(simulated_totals_utopisch[i] >= simulated_totals_utopisch[i + 1] for i in range(len(simulated_totals_utopisch) - 1)),
            "Reductietrend is niet consistent."
        )

if __name__ == "__main__":
    unittest.main()
