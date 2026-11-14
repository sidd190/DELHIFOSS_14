import importlib.util
import itertools
import pathlib
import unittest
from fractions import Fraction as F
spec = importlib.util.spec_from_file_location('payoff', pathlib.Path(__file__).parents[1] / 'game-theory/payoff.py')
payoff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(payoff)


class DominanceTests(unittest.TestCase):
    def test_talk_result(self):
        r = payoff.solve([[2, 8], [4, 5]])
        self.assertEqual(r['dominated_attacks'], [dict(dominated=0, by=1)])
        self.assertEqual(r['dominated_defenses'], [])
        self.assertEqual(r['best_defenses'], [1])
        self.assertEqual(r['worst_case_loss'], 5)
        self.assertEqual(r['pure_saddle_points'], [dict(defense=1, attack=1, loss=5)])

    def test_ties_are_not_strict_dominance(self):
        r = payoff.solve([[5, 5], [5, 5]])
        self.assertEqual(r['dominated_attacks'], [])
        self.assertEqual(r['dominated_defenses'], [])
        self.assertEqual(r['best_defenses'], [0, 1])
        self.assertEqual(len(r['pure_saddle_points']), 4)

    def test_crossing_preferences_do_not_invent_dominance(self):
        r = payoff.solve([[1, 6], [7, 2]])
        self.assertEqual(r['dominated_attacks'], [])
        self.assertEqual(r['dominated_defenses'], [])
        self.assertEqual(r['pure_saddle_points'], [])
        self.assertEqual(r['best_defenses'], [0])

    def test_reverse_dominance(self):
        r = payoff.solve([[8, 2], [5, 4]])
        self.assertEqual(r['dominated_attacks'], [dict(dominated=1, by=0)])

    def test_defender_dominance_uses_smaller_losses(self):
        self.assertEqual(payoff.solve([[1, 2], [4, 5]])['dominated_defenses'], [dict(dominated=1, by=0)])

    def test_decimal_input(self):
        self.assertEqual(payoff.solve([['0.2', '0.8'], ['0.4', '0.5']])['worst_case_loss'], F(1, 2))

    def test_reported_saddles_have_no_improving_pure_deviation(self):
        for a, b, c, d in itertools.product(range(-2, 4), repeat=4):
            m = [[a,b],[c,d]]
            for point in payoff.solve(m)['pure_saddle_points']:
                i,j,v = point['defense'],point['attack'],point['loss']
                self.assertTrue(all(m[row][j] >= v for row in range(2)))
                self.assertTrue(all(m[i][col] <= v for col in range(2)))

    def test_invalid_input(self):
        for m in ([[1,2]], [[1,2,3],[4,5,6]], [['NaN',0],[0,0]], [['inf',0],[0,0]]):
            with self.assertRaises(ValueError): payoff.solve(m)
