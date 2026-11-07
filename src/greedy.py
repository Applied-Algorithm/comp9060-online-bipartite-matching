"""Greedy — owner: Miskat
Each arrival takes the first available neighbour, or stays unmatched if
none are free. Deterministic. Guaranteed at least 50% of optimal.
"""

def run(adj, arrival_order, n_right, seed=None, capacity=1):
    """Return (matching, size). `capacity` is the b-matching capacity (1 = ordinary)."""
    raise NotImplementedError("Implement Greedy")
