"""
Phase 4 — Compare BFS, DFS, and A* fairly.

We run the same start→goal pairs on all three algorithms and measure:
  - travel time (minutes) of the path found
  - hops
  - nodes expanded
  - runtime

Also saves simple bar charts with matplotlib.
"""

from __future__ import annotations

from typing import Callable, List, Tuple

import matplotlib.pyplot as plt

from network import STOPS
from search import SearchResult, astar, bfs, dfs


# Routes chosen to cover different Nairobi corridors
TEST_ROUTES: List[Tuple[str, str]] = [
    ("cbd", "rongai"),
    ("cbd", "embakasi"),
    ("westlands", "rongai"),
    ("kasarani", "karen"),
    ("kangemi", "donholm"),
    ("parklands", "embakasi"),
]

ALGORITHMS: List[Tuple[str, Callable[[str, str], SearchResult]]] = [
    ("BFS", bfs),
    ("DFS", dfs),
    ("A*", astar),
]


def route_label(start: str, goal: str) -> str:
    return f"{STOPS[start]['name']} -> {STOPS[goal]['name']}"


def run_all_comparisons() -> List[SearchResult]:
    """Run every algorithm on every test route."""
    results: List[SearchResult] = []
    for start, goal in TEST_ROUTES:
        for _name, fn in ALGORITHMS:
            results.append(fn(start, goal))
    return results


def print_comparison_table(results: List[SearchResult]) -> None:
    """Print one readable table per route."""
    print("=" * 78)
    print("PHASE 4 - ALGORITHM COMPARISON")
    print("=" * 78)

    for start, goal in TEST_ROUTES:
        route_results = [r for r in results if r.start == start and r.goal == goal]
        print()
        print(f"Route: {route_label(start, goal)}")
        print("-" * 78)
        print(
            f"{'Algo':<6} {'Hops':>6} {'Time(min)':>10} "
            f"{'Expanded':>10} {'Runtime(ms)':>12}  Path"
        )
        print("-" * 78)

        for r in route_results:
            hops = "-" if r.hops is None else str(r.hops)
            mins = "-" if r.time_cost_minutes is None else str(r.time_cost_minutes)
            path = (
                " -> ".join(STOPS[s]["name"] for s in r.path)
                if r.path
                else "(none)"
            )
            # Keep path short on one line for the table
            if len(path) > 42:
                path = path[:39] + "..."

            print(
                f"{r.algorithm:<6} {hops:>6} {mins:>10} "
                f"{r.nodes_expanded:>10} {r.runtime_seconds * 1000:>12.3f}  {path}"
            )


def print_takeaways(results: List[SearchResult]) -> None:
    """Short, honest summary of what the numbers usually show."""
    print()
    print("=" * 78)
    print("TAKEAWAYS (for your report)")
    print("=" * 78)
    print(
        "- BFS: lowest or tied hops. Travel time is often NOT the best.\n"
        "- DFS: unpredictable path quality; sometimes lucky, sometimes worse.\n"
        "- A*: lowest (or tied) travel time in minutes - what passengers usually want.\n"
        "- Nodes expanded / runtime: on this small graph differences are tiny;\n"
        "  A*'s real advantage grows on larger networks."
    )


def plot_metric(
    results: List[SearchResult],
    metric: str,
    title: str,
    ylabel: str,
    filename: str,
) -> None:
    """
    Grouped bar chart: one group per route, three bars (BFS/DFS/A*).

    metric: 'time_cost_minutes' | 'nodes_expanded' | 'runtime_ms'
    """
    labels = [route_label(s, g) for s, g in TEST_ROUTES]
    x = range(len(TEST_ROUTES))
    width = 0.25

    fig, ax = plt.subplots(figsize=(12, 5))

    for i, (algo_name, _) in enumerate(ALGORITHMS):
        values = []
        for start, goal in TEST_ROUTES:
            match = next(
                r
                for r in results
                if r.start == start and r.goal == goal and r.algorithm == algo_name
            )
            if metric == "runtime_ms":
                values.append(match.runtime_seconds * 1000)
            elif metric == "time_cost_minutes":
                values.append(
                    match.time_cost_minutes if match.time_cost_minutes is not None else 0
                )
            else:
                values.append(getattr(match, metric))

        positions = [pos + (i - 1) * width for pos in x]
        ax.bar(positions, values, width=width, label=algo_name)

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(filename, dpi=140)
    plt.close(fig)
    print(f"Saved chart: {filename}")


def save_charts(results: List[SearchResult]) -> None:
    plot_metric(
        results,
        metric="time_cost_minutes",
        title="Travel time of path found (lower is better for passengers)",
        ylabel="Minutes",
        filename="comparison_travel_time.png",
    )
    plot_metric(
        results,
        metric="nodes_expanded",
        title="Nodes expanded during search (lower = less work)",
        ylabel="Nodes expanded",
        filename="comparison_nodes_expanded.png",
    )
    plot_metric(
        results,
        metric="runtime_ms",
        title="Runtime (small graph — differences may be tiny)",
        ylabel="Milliseconds",
        filename="comparison_runtime.png",
    )


if __name__ == "__main__":
    all_results = run_all_comparisons()
    print_comparison_table(all_results)
    print_takeaways(all_results)
    print()
    save_charts(all_results)
    print()
    print("Phase 4 done. Open the .png files in this folder to see the graphs.")
