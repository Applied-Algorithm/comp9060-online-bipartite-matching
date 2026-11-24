
"""Plots for Online Bipartite Matching experiments.

Owner: Radhika

Reads experiment results from a CSV file and generates
charts comparing matching quality and running time.

The CSV column names will be confirmed once the
experiment runner is implemented.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# File locations
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = PROJECT_ROOT / "results" / "results.csv"
PLOTS_DIR = PROJECT_ROOT / "results" / "plots"


def main():
    """Generate plots from the experiment results."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    if not RESULTS_FILE.exists():
        print("Results CSV not found. Waiting for experiment data.")
        return

    df = pd.read_csv(RESULTS_FILE)
    print(f"Loaded {len(df)} experiment results.")

    # Compare graph sizes separately for each graph type and capacity.
    for (graph_type, capacity), subset in df.groupby(
        ["graph_type", "capacity"]
    ):
        plot_matching_ratio(subset)
        plt_path = PLOTS_DIR / f"matching_ratio_{graph_type}_b{capacity}.png"
        (RESULTS_FILE.parent / "matching_ratio.png").replace(plt_path)

        plot_runtime(subset)
        plt_path = PLOTS_DIR / f"runtime_{graph_type}_b{capacity}.png"
        (RESULTS_FILE.parent / "runtime.png").replace(plt_path)

    plot_graph_types(df)
    plot_capacity(df)

    print("All plots generated successfully!")

def plot_matching_ratio(df):
    """Plot matching ratio against graph size."""
    for algorithm in df["algorithm"].unique():
        data = df[df["algorithm"] == algorithm]
        grouped = data.groupby("size")["matching_ratio"].mean()
        plt.plot(grouped.index, grouped.values, marker="o", label=algorithm)

    plt.xlabel("Graph Size")
    plt.ylabel("Matching Ratio")
    plt.title("Matching Ratio vs Graph Size")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_FILE.parent / "matching_ratio.png", dpi=300)
    plt.close()

def plot_runtime(df):
    """Plot average runtime against graph size."""
    plt.figure(figsize=(8, 5))

    for algorithm in df["algorithm"].unique():
        data = df[df["algorithm"] == algorithm]
        grouped = data.groupby("size")["runtime"].mean()

        plt.plot(grouped.index, grouped.values,
                 marker="o", label=algorithm)

    plt.xlabel("Graph Size")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime vs Graph Size")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_FILE.parent / "runtime.png", dpi=300)
    plt.close()

def plot_graph_types(df):
    """Compare matching ratios across graph types."""

    # Compare ordinary matching at the same graph size.
    data = df[(df["capacity"] == 1) & (df["size"] == 100)]

    grouped = data.groupby(
        ["graph_type", "algorithm"]
    )["matching_ratio"].mean().unstack()

    ax = grouped.plot(kind="bar", figsize=(9, 5))

    ax.set_xlabel("Graph Type")
    ax.set_ylabel("Average Matching Ratio")
    ax.set_title("Algorithm Performance Across Graph Types")
    ax.set_ylim(0, 1)
    ax.legend(title="Algorithm")

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "graph_types.png", dpi=300)
    plt.close()

def plot_capacity(df):
    """Compare matching ratios across different capacities."""

    data = df[(df["size"] == 100) &
              (df["graph_type"] == "sparse")]

    plt.figure(figsize=(8, 5))

    for algorithm in data["algorithm"].unique():
        subset = data[data["algorithm"] == algorithm]
        grouped = subset.groupby("capacity")["matching_ratio"].mean()

        plt.plot(grouped.index, grouped.values,
                 marker="o", label=algorithm)

    plt.xlabel("Capacity")
    plt.ylabel("Average Matching Ratio")
    plt.title("Algorithm Performance vs Capacity")
    plt.xticks([1, 2, 3, 5])
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "capacity.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
