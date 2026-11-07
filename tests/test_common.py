"""Tests for the shared interface in src/common.py.

Run: python3 -m unittest discover -s tests -v
"""

import unittest

from src.common import check_matching, matching_size, validate_graph

""""Small hand-checked graph, used by every algorithm test too.
Left 0 -> right 0, 1; left 1 -> right 0 only; left 2 -> right 1 only.
Greedy in arrival order 0, 1, 2 matches 0->0, then 1 is stuck, 2->1 (size 2).
Offline optimal also gets 2 here (0->1, 1->0 leaves 2 unmatched, or 0->0, 2->1).""""
SMALL_ADJ = {0: [0, 1], 1: [0], 2: [1]}
SMALL_ARRIVAL = [0, 1, 2]
N_RIGHT = 2


class TestCommon(unittest.TestCase):
    def test_validate_accepts_small_graph(self):
        self.assertTrue(validate_graph(SMALL_ADJ, SMALL_ARRIVAL, N_RIGHT))

    def test_validate_rejects_bad_right_vertex(self):
        with self.assertRaises(ValueError):
            validate_graph({0: [99]}, [0], N_RIGHT)

    def test_validate_rejects_missing_arrival(self):
        with self.assertRaises(ValueError):
            validate_graph(SMALL_ADJ, [0, 1], N_RIGHT)

    def test_matching_size(self):
        self.assertEqual(matching_size({0: 0, 2: 1}), 2)

    def test_check_matching_accepts_legal_matching(self):
        self.assertTrue(check_matching({0: 0, 2: 1}, SMALL_ADJ, N_RIGHT))

    def test_check_matching_rejects_non_edge(self):
        with self.assertRaises(ValueError):
            check_matching({1: 1}, SMALL_ADJ, N_RIGHT)

    def test_check_matching_rejects_over_capacity(self):
        # Right 0 used twice with capacity 1.
        with self.assertRaises(ValueError):
            check_matching({0: 0, 1: 0}, SMALL_ADJ, N_RIGHT, capacity=1)

    def test_check_matching_allows_b_matching(self):
        self.assertTrue(
            check_matching({0: 0, 1: 0}, SMALL_ADJ, N_RIGHT, capacity=2)
        )


if __name__ == "__main__":
    unittest.main()
