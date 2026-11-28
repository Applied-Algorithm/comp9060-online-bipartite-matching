"""Experiment runner — owner: Miskat

Loops over graph type, size and algorithm, runs each at least 5 times,
times it, and saves matches, percentage of offline optimal, and running
time to results/results.csv. Same graph (same seed) to every algorithm.

Do not run the full sizes until the small tests in tests/ pass.
Start with a size-50 trial only, to check the CSV and timing work.
How to run:
    python -m src.run_experiments          full run (all sizes)
    python -m src.run_experiments small    trial run (sizes 50 and 100 only)

"""

import csv
import sys
import time
from pathlib import Path

from src import generators, greedy, offline_optimal, random_greedy, ranking

SIZES = [50, 100, 250, 500, 1000]
GRAPH_KINDS = ["sparse", "dense", "adversarial"]
RUNS_PER_SETUP = 5
CAPACITIES = [1, 2, 3, 5]  # 1 = ordinary matching; 2, 3, 5 = b-matching

ALGORITHMS = {
    "greedy": greedy.run,
    "random_greedy": random_greedy.run,
    "ranking": ranking.run,
    "offline_optimal": offline_optimal.run,
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = PROJECT_ROOT / "results" / "results.csv"

FIELDNAMES = [
    "graph_type",
    "size",
    "n",
    "capacity",
    "run",
    "algorithm",
    "matches",
    "optimal_matches",
    "matching_ratio",
    "percent_of_optimal",
    "runtime",
    "time_seconds",
]



def main():
    sizes = SIZES
    if len(sys.argv) > 1 and sys.argv[1] == "small":
        sizes = [50, 100]
        print("Small trial run: sizes 50 and 100 only")

    rows = []

    for kind in GRAPH_KINDS:
        for size in sizes:
            for capacity in CAPACITIES:
                for run_number in range(1, RUNS_PER_SETUP + 1):
                    seed = run_number
                    adj, arrival_order, n_right = generators.generate(
                        size, kind, seed=seed
                    )

                    # Offline Optimal first, on this exact graph.
                    # Its size is the answer key for every ratio below.
                    start = time.perf_counter()
                    _, optimal_size = offline_optimal.run(
                        adj, arrival_order, n_right, seed=seed, capacity=capacity
                    )
                    optimal_runtime = time.perf_counter() - start

                    for name, run_algorithm in ALGORITHMS.items():
                        if name == "offline_optimal":
                            matches = optimal_size
                            runtime = optimal_runtime
                        else:
                            start = time.perf_counter()
                            _, matches = run_algorithm(
                                adj,
                                arrival_order,
                                n_right,
                                seed=seed,
                                capacity=capacity,
                            )
                            runtime = time.perf_counter() - start

                        if optimal_size > 0:
                            ratio = matches / optimal_size
                        else:
                            ratio = 1.0

                        rows.append(
                            {
                                "graph_type": kind,
                                "size": size,
                                "n": size,
                                "capacity": capacity,
                                "run": run_number,
                                "algorithm": name,
                                "matches": matches,
                                "optimal_matches": optimal_size,
                                "matching_ratio": round(ratio, 6),
                                "percent_of_optimal": round(ratio * 100, 2),
                                "runtime": round(runtime, 6),
                                "time_seconds": round(runtime, 6),
                            }
                        )

                print(
                    f"done: {kind} size={size} capacity={capacity} "
                    f"({RUNS_PER_SETUP} runs)"
                )

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {RESULTS_FILE}")



if __name__ == "__main__":
    main()
