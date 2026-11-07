"""Experiment runner — owner: Miskat

Loops over graph type, size and algorithm, runs each at least 5 times,
times it, and saves matches, percentage of offline optimal, and running
time to results/results.csv. Same graph (same seed) to every algorithm.

Do not run the full sizes until the small tests in tests/ pass.
Start with a size-50 trial only, to check the CSV and timing work.
"""

SIZES = [50, 100, 250, 500, 1000]
GRAPH_KINDS = ["sparse", "dense", "adversarial"]
RUNS_PER_SETUP = 5
CAPACITIES = [1, 2, 3, 5]  # 1 = ordinary matching; 2, 3, 5 = b-matching


def main():
    raise NotImplementedError(
        "Implement run_experiments: loop sizes x kinds x algorithms x runs, "
        "write results/results.csv with matches, % of optimal, runtime"
    )


if __name__ == "__main__":
    main()
