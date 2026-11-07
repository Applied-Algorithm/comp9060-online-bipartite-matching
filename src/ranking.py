"""RANKING — owner: Radhika

Shuffle the right side once at the start into a random priority order
(fixed before any arrival). Each arrival takes the highest-ranked neighbour
that is still free. Use `seed` so the ranking is reproducible.
Proven at least 63.2% (1 - 1/e) of optimal in the worst case.
"""

def run(adj, arrival_order, n_right, seed=None, capacity=1):
    """Return (matching, size). `capacity` is the b-matching capacity (1 = ordinary)."""
    raise NotImplementedError("Implement RANKING")
