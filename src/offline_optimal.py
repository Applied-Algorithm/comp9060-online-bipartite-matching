"""Offline Optimal — owner: Marvelous

Hopcroft-Karp. Sees the whole graph at once and finds the maximum matching.
Used only as the answer key: every percentage in the results is measured
against this number, so it has to be correct. It must never be beaten by
an online algorithm on the same graph — that is the first test to write.

For b-matching (capacity > 1), the baseline is offline optimal b-matching
by max flow, not Hopcroft-Karp. 
"""


from collections import deque


def run(adj, arrival_order, n_right, seed=None, capacity=1):
    """Return (matching, size). `arrival_order` is ignored (offline sees all).

    `capacity=1`: Hopcroft-Karp. `capacity>1`: max-flow b-matching baseline.
    """
    if capacity != 1:
        raise NotImplementedError("capacity > 1 is the shared max-flow step")

    lefts = sorted(adj.keys())
    pair_left = {left: -1 for left in lefts}
    pair_right = [-1] * n_right
    dist = {}
    INF = float("inf")

    def bfs():
        queue = deque()
        for left in lefts:
            if pair_left[left] == -1:
                dist[left] = 0
                queue.append(left)
            else:
                dist[left] = INF
        found = False
        while queue:
            left = queue.popleft()
            for right in adj[left]:
                other = pair_right[right]
                if other != -1 and dist[other] == INF:
                    dist[other] = dist[left] + 1
                    queue.append(other)
                if other == -1:
                    found = True
        return found

    def dfs(left):
        for right in adj[left]:
            other = pair_right[right]
            if other == -1 or (dist[other] == dist[left] + 1 and dfs(other)):
                pair_left[left] = right
                pair_right[right] = left
                return True
        dist[left] = INF
        return False

    while bfs():
        for left in lefts:
            if pair_left[left] == -1:
                dfs(left)

    matching = {left: right for left, right in pair_left.items() if right != -1}
    return matching, len(matching)