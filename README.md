# COMP 9060 — Online Bipartite Matching: A Survey and Experimental Comparison

Topic: Online Bipartite Matching, Option A (Survey), for Hao Ma. Worth 25%.
Final deliverables: a 5-6 page paper in ACM format, a code repository, and a
20-minute presentation with no scripts. Presentation and report date: Dec 1
(course outline). Any team member can be asked about any part in Q&A.

## The one interface everything must agree on

Agreed before anyone codes, so all the code fits together (see `src/common.py`):

- A graph is an adjacency list: `adj[left_vertex] = [right neighbours]`.
  Left vertices are `0..n-1`, right vertices are `0..n-1`, `n` on each side.
- `arrival_order` is the list of left vertices in the order they arrive.
- Every algorithm has the same signature:

```python
run(adj, arrival_order, n_right, seed=None, capacity=1) -> (matching, size)
```

  `matching` maps each matched left vertex to one right vertex.
  `capacity=1` is ordinary matching; `capacity=2, 3, 5` is b-matching, where
  each right vertex may be used up to `capacity` times.
- Offline Optimal takes the same inputs (it sees the whole graph at once)
  so it can be swapped in as the answer key in the experiment runner.
## Proposed split

From the updated coding plan:

| Owner | Files | Notes |
|---|---|---|
| Marvelous | `src/generators.py`, `src/offline_optimal.py` (capacity 1) | He writes all 3 graph types in generators.py, plus the generate helper. He also writes 1 small test for Offline Optimal. |
| Miskat | `src/greedy.py`, `src/random_greedy.py`, `src/run_experiments.py` | She also does the b-matching capacity part in her own files, and 1 small test for Greedy. |
| Radhika | `src/ranking.py`, `src/plots.py` (made later) | She also does the b-matching capacity part in ranking.py, and 1 small test for RANKING. plots.py is made later, after results.csv exists, to make the charts. |
| Together | GitHub setup, offline b-matching by max flow in `src/offline_optimal.py` | All three also run the tests together, run the full experiments together, and check results.csv together. |


## Algorithms (all in Python, all fed the exact same graphs)

1. Offline Optimal — Hopcroft-Karp, sees the full graph, answer key only.
2. Greedy — each arrival takes the first available neighbour.
3. Random Greedy — each arrival takes a random available neighbour.
4. RANKING — one random ranking of the offline side fixed in advance; each
   arrival takes the highest-ranked available neighbour.
5. b-matching extensions of Greedy and RANKING at b = 2, 3, 5, with offline
   optimal b-matching by max flow as the baseline.

## Experiments promised in the proposal

- Graph types: sparse, dense, adversarial (early arrivals flexible, late arrivals
  have exactly one option, so Greedy gets trapped).
- Sizes: 50, 100, 250, 500, 1000 on each side.
- At least 5 runs per setup, same graph to every algorithm.
- Metrics: matches made, percentage of offline optimal, running time.
- Results go in tables and charts and are compared back to the theory bounds:
  Greedy at least 50% of optimal, RANKING at least 63.2% (1 - 1/e).

## Research questions

1. Does RANKING beat Greedy and Random Greedy in practice, or only in theory?
2. How close does each get to its bound?
3. How much does arrival order hurt — random vs adversarial?
4. How does running time scale with size, and is a small gain worth the time cost?
5. For b-matching, how do Greedy and RANKING do against offline optimal b-matching?

## Workflow

- Before committing, set your identity for this repository (replace the values
  with your own):

```bash
git config user.name "Your Name"
git config user.email "you@example.com"
```

- Work in order: (1) lock the interface and generators, (2) code the 4 algorithms
  in parallel, (3) test on small hand-checked graphs, (4) add b-matching,
  (5) run the full experiments, (6) analyse, write the paper, build slides.

## Timeline

- Nov 6-8: repo created, all three added, interface agreed, generators started
- Nov 9-12: first working versions of all four algorithms, small tests passing
- Nov 13-15: b-matching extensions done
- Nov 16-19: full experiments run, CSVs and plots saved in `results/`
- Nov 20-23: analysis and paper sections drafted (before the Nov 24 COMP 9060
  assignment deadline)
- Nov 24-27: full paper assembled in ACM format, slides built
- Nov 28-30: rehearse the 20 minutes and prep Q&A on every algorithm
- Dec 1: presentation and report
- test Miskat
