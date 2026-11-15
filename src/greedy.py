"""Greedy online bipartite matching - Miskat.

Each arriving left vertex takes its first available right neighbour.
A right vertex can accept up to `capacity` left vertices.
"""


def run(adj, arrival_order, n_right, seed=None, capacity=1):
    """Return (matching, size) using the agreed interface in common.py."""
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
        raise ValueError("capacity must be a positive integer")

    # The count tells us how many riders have taken each driver.
    used_count = [0] * n_right
    matching = {}

    # Riders arrive one by one. We never change an earlier decision.
    for left in arrival_order:
        for right in adj[left]:
            if used_count[right] < capacity:
                matching[left] = right
                used_count[right] += 1
                break

    return matching, len(matching)
