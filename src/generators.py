"""Graph generators - Owner : Marvelous

Proposal definitions:
- sparse: few edges per arrival.
- dense: many edges per arrival.
- adversarial: early arrivals are flexible (many choices), late arrivals have
  exactly one option, so Greedy gets trapped by an early match that blocks
  a later arrival."""


def sparse_graph(n, seed=None):
    """Sparse graph: few edges per arrival."""
    raise NotImplementedError("Implement sparse_graph: lock 'few edges' on the call first")


def dense_graph(n, seed=None):
    """Dense graph: many edges per arrival."""
    raise NotImplementedError("Implement dense_graph: lock 'many edges' on the call first")


def adversarial_graph(n, seed=None):
    """Adversarial graph that traps Greedy.
    Early arrivals flexible, late arrivals have exactly one option.
    """
    raise NotImplementedError("Implement adversarial_graph: lock the construction on the call first")


def generate(n, kind, seed=None):
    """Generate a graph of the given kind: 'sparse', 'dense' or 'adversarial'."""
    kinds = {"sparse": sparse_graph, "dense": dense_graph, "adversarial": adversarial_graph}
    if kind not in kinds:
        raise ValueError(f"unknown graph kind {kind!r}, expected one of {sorted(kinds)}")
    return kinds[kind](n, seed=seed)
