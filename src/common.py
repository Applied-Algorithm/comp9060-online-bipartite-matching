"""Shared types and the one interface every algorithm must follow.

Graph representation (agreed before anyone codes):
  adj: dict[int, list[int]] — adj[left] = right-side neighbours of `left`.
       Left vertices are 0..n-1, right vertices are 0..n-1.
  arrival_order: list[int] — left vertices in the order they arrive.
  n_right: int — number of vertices on the right side.

Every algorithm:
  run(adj, arrival_order, n_right, seed=None, capacity=1) -> (matching, size)
  matching: dict[int, int] — matched left vertex -> one right vertex.
  size: int — number of matches, len(matching).
  capacity=1 is ordinary matching. capacity=2, 3, 5 is b-matching: each right
  vertex may be used up to `capacity` times. A left vertex still matches at
  most once, so the return type does not change for b-matching.

Offline Optimal takes the same inputs so it can be swapped in as the answer
key in the experiment runner, even though it sees the whole graph at once.
"""



def validate_graph(adj, arrival_order, n_right):
    """Check a graph matches the agreed format. Raises ValueError if not.

    Used by the experiment runner and by every algorithm's tests, so a bad
    generator fails loudly instead of silently producing wrong numbers.
    """
    if n_right <= 0:
        raise ValueError("n_right must be positive")
    if sorted(arrival_order) != sorted(adj.keys()):
        raise ValueError("arrival_order must list every left vertex exactly once")
    for left, neighbours in adj.items():
        if left < 0:
            raise ValueError(f"left vertex {left} must be >= 0")
        if len(set(neighbours)) != len(neighbours):
            raise ValueError(f"left vertex {left} has duplicate neighbours")
        for right in neighbours:
            if not 0 <= right < n_right:
                raise ValueError(
                    f"right vertex {right} for left {left} outside 0..{n_right - 1}"
                )
    return True


def matching_size(matching):
    """Number of matches in a matching dict."""
    return len(matching)


def check_matching(matching, adj, n_right, capacity=1):
    """Check a matching is legal for the graph. Raises ValueError if not."""
    validate_graph(adj, list(adj.keys()), n_right)
    used = {}
    for left, right in matching.items():
        if left not in adj:
            raise ValueError(f"matched left vertex {left} is not in the graph")
        if right not in adj[left]:
            raise ValueError(f"left {left} is not adjacent to right {right}")
        used[right] = used.get(right, 0) + 1
        if used[right] > capacity:
            raise ValueError(f"right vertex {right} used more than {capacity} times")
    return True
