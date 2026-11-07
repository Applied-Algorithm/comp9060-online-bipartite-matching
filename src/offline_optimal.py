"""Offline Optimal — owner: Marvelous

Hopcroft-Karp. Sees the whole graph at once and finds the maximum matching.
Used only as the answer key: every percentage in the results is measured
against this number, so it has to be correct. It must never be beaten by
an online algorithm on the same graph — that is the first test to write.

For b-matching (capacity > 1), the baseline is offline optimal b-matching
by max flow, not Hopcroft-Karp. 
"""


def run(adj, arrival_order, n_right, seed=None, capacity=1):
    """Return (matching, size). `arrival_order` is ignored (offline sees all).

    `capacity=1`: Hopcroft-Karp. `capacity>1`: max-flow b-matching baseline.
    """
    raise NotImplementedError("Implement Offline Optimal (Hopcroft-Karp)")
