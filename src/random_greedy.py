"""Random Greedy — owner: Miskat
Same as Greedy, but each arrival takes a uniformly random available
neighbour. Use `seed` so runs are reproducible.
"""

import random


def run(adj, arrival_order, n_right, seed=None, capacity=1):
    """Return (matching, size) using the agreed interface in common.py."""
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
        raise ValueError("capacity must be a positive integer")

    rng = random.Random(seed)
    used_count = [0] * n_right
    matching = {}

    for left in arrival_order:
        # Choose again for every new rider (unlike fixed-priority RANKING).
        available = [right for right in adj[left] if used_count[right] < capacity]
        if available:
            right = rng.choice(available)
            matching[left] = right
            used_count[right] += 1

    return matching, len(matching)
