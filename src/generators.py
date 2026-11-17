"""Graph generators - Owner : Marvelous

Proposal definitions:
- sparse: few edges per arrival.
- dense: many edges per arrival.
- adversarial: early arrivals are flexible (many choices), late arrivals have
  exactly one option, so Greedy gets trapped by an early match that blocks
  a later arrival."""
import random


def sparse_graph(n, seed=None):
    """Sparse graph: few edges per arrival."""
    rng = random.Random(seed)
    adj={}
    for left in range(n):
        how_many = rng.randint(1, min(2, n))
        neighbours = sorted(rng.sample(range(n), how_many))
        adj[left] = neighbours
    arrival_order = list(range(n))
    return adj, arrival_order, n

def dense_graph(n, seed=None):
    """Dense graph: many edges per arrival."""
    
    rng = random.Random(seed)
    adj = {}
    for left in range(n):
        how_many = n // 2
        neighbours = sorted(rng.sample(range(n), how_many))
        adj[left] = neighbours
    arrival_order = list(range(n))
    return adj, arrival_order, n
    

def adversarial_graph(n, seed=None):
    """Adversarial graph that traps Greedy.
    Early arrivals flexible, late arrivals have exactly one option.
    """
    adj = {}
    half = n // 2
    for left in range(n):
        if left < half:
            adj[left] = list(range(n))
        else:
            adj[left] = [left - half]
    arrival_order = list(range(n))
    return adj, arrival_order, n
 

def generate(n, kind, seed=None):
    """Generate a graph of the given kind: 'sparse', 'dense' or 'adversarial'."""
    kinds = {"sparse": sparse_graph, "dense": dense_graph, "adversarial": adversarial_graph}
    if kind not in kinds:
        raise ValueError(f"unknown graph kind {kind!r}, expected one of {sorted(kinds)}")
    return kinds[kind](n, seed=seed)
