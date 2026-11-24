"""Offline Optimal — owner: Marvelous

Hopcroft-Karp. Sees the whole graph at once and finds the maximum matching.
Used only as the answer key: every percentage in the results is measured
against this number, so it has to be correct. It must never be beaten by
an online algorithm on the same graph — that is the first test to write.

For b-matching (capacity > 1), the baseline is offline optimal b-matching
by max flow, not Hopcroft-Karp. 
"""


from collections import deque

def max_flow_b_matching(adj, n_right, capacity):
    """Offline optimal b-matching by max flow (Dinic).
    Source -> each left (cap 1), left -> right edges (cap 1),
    each right -> sink (cap = capacity). Each unit of flow is a match.
    """
    lefts = sorted(adj.keys())
    n_left = len(lefts)
    source = 0
    left_start = 1
    right_start = 1 + n_left
    sink = right_start + n_right
    n_nodes = sink + 1

    graph = [[] for _ in range(n_nodes)]

    def add_edge(u, v, cap):
        graph[u].append([v, cap, len(graph[v])])
        graph[v].append([u, 0, len(graph[u]) - 1])
        return len(graph[u]) - 1

    for i, left in enumerate(lefts):
        add_edge(source, left_start + i, 1)
    for r in range(n_right):
        add_edge(right_start + r, sink, capacity)

    left_right_edges = []
    for i, left in enumerate(lefts):
        u = left_start + i
        for right in adj[left]:
            idx = add_edge(u, right_start + right, 1)
            left_right_edges.append((left, right, u, idx))

    level = [0] * n_nodes
    it = [0] * n_nodes

    def bfs():
        for i in range(n_nodes):
            level[i] = -1
        level[source] = 0
        queue = deque([source])
        while queue:
            v = queue.popleft()
            for to, cap, rev in graph[v]:
                if cap > 0 and level[to] == -1:
                    level[to] = level[v] + 1
                    queue.append(to)
        return level[sink] != -1

    def dfs(v, f):
        if v == sink:
            return f
        while it[v] < len(graph[v]):
            i = it[v]
            to, cap, rev = graph[v][i]
            if cap > 0 and level[to] == level[v] + 1:
                pushed = dfs(to, min(f, cap))
                if pushed:
                    graph[v][i][1] -= pushed
                    graph[to][rev][1] += pushed
                    return pushed
            it[v] += 1
        return 0

    while bfs():
        it = [0] * n_nodes
        while True:
            pushed = dfs(source, float("inf"))
            if not pushed:
                break

    matching = {}
    for left, right, u, idx in left_right_edges:
        if graph[u][idx][1] == 0:
            matching[left] = right
    return matching, len(matching)

def run(adj, arrival_order, n_right, seed=None, capacity=1):
    """Return (matching, size). `arrival_order` is ignored (offline sees all).

    `capacity=1`: Hopcroft-Karp. `capacity>1`: max-flow b-matching baseline.
    """
    if capacity != 1:
        return max_flow_b_matching(adj, n_right, capacity)


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