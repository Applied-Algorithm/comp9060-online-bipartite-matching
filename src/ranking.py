"""RANKING — owner: Radhika

Shuffle the right side once at the start into a random priority order
(fixed before any arrival). Each arrival takes the highest-ranked neighbour
that is still free. Use `seed` so the ranking is reproducible.
Proven at least 63.2% (1 - 1/e) of optimal in the worst case.
"""

import random
def run(adj, arrival_order, n_right, seed=None, capacity=1):
    """Return (matching, size) using the interface in common.py."""

    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
        raise ValueError("capacity must be a positive integer")

    # Randomly rank the right vertices once.
    rng = random.Random(seed)
    ranking = list(range(n_right))
    rng.shuffle(ranking)

    # Lower number means higher priority.
    priority = {right: i for i, right in enumerate(ranking)}

    used_count = [0] * n_right
    matching = {}

    # Process left vertices in arrival order.
    for left in arrival_order:
        best_right = None

        for right in adj[left]:
            if used_count[right] < capacity:
                if best_right is None or priority[right] < priority[best_right]:
                    best_right = right

        if best_right is not None:
            matching[left] = best_right
            used_count[best_right] += 1

    return matching, len(matching)
