"""Tests for the algorithms in src/.

Each algorithm is run on the small graph from test_common.
Two things are checked:
- the matching it returns is legal (check_matching passes);
- no online algorithm beats offline optimal on the same graph.
An algorithm that is not written yet is skipped.

Run: python -m unittest discover -s tests -p "test_algorithms.py" -v

"""

import unittest

from src import greedy, offline_optimal, random_greedy, ranking
from src.common import check_matching
from test_common import N_RIGHT, SMALL_ADJ, SMALL_ARRIVAL

ALGORITHMS = [greedy, random_greedy, ranking, offline_optimal]
ONLINE = [greedy, random_greedy, ranking]


def run_small(module):
    """Run one algorithm on the small graph.

    Returns (matching, size), or None if it is not written yet.
    """
    try:
        return module.run(SMALL_ADJ, SMALL_ARRIVAL, N_RIGHT, seed=0)
    except NotImplementedError:
        return None


class TestAlgorithms(unittest.TestCase):
    def test_each_algorithm_on_small_graph(self):
        for module in ALGORITHMS:
            result = run_small(module)
            if result is None:
                print(f"SKIP {module.__name__}: not implemented yet")
                continue
            matching, size = result
            self.assertEqual(size, len(matching))
            self.assertTrue(check_matching(matching, SMALL_ADJ, N_RIGHT))
            self.assertLessEqual(size, N_RIGHT)

    def test_offline_optimal_never_beaten(self):
        result = run_small(offline_optimal)
        if result is None:
            self.skipTest("offline_optimal not implemented yet")
        _, opt_size = result
        for module in ONLINE:
            result = run_small(module)
            if result is None:
                continue
            _, size = result
            self.assertLessEqual(size, opt_size)


if __name__ == "__main__":
    unittest.main()
