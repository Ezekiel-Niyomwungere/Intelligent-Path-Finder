"""
Phase 5 — Demo: find routes and explain what each algorithm did.

Usage examples:
  python demo.py
  python demo.py cbd rongai
  python demo.py westlands embakasi
"""

from __future__ import annotations

import sys
from typing import List, Tuple

from network import GRAPH, STOPS
from search import SearchResult, astar, bfs, dfs
from visualize import plot_route


def list_stops() -> None:
    print("Available stops:")
    for stop_id, info in STOPS.items():
        print(f"  {stop_id:<12} {info['name']}")


def parse_args(argv: List[str]) -> Tuple[str, str]:
    if len(argv) == 1:
        return "cbd", "rongai"

    if len(argv) == 2 and argv[1] in {"-h", "--help"}:
        print(__doc__)
        list_stops()
        sys.exit(0)

    if len(argv) != 3:
        print("Usage: python demo.py [start_id] [goal_id]")
        print("Example: python demo.py cbd rongai")
        print()
        list_stops()
        sys.exit(1)

    start, goal = argv[1].lower(), argv[2].lower()
    if start not in GRAPH or goal not in GRAPH:
        print("Unknown stop id.")
        print()
        list_stops()
        sys.exit(1)

    return start, goal


def step_by_step(result: SearchResult) -> None:
    start_name = STOPS[result.start]["name"]
    goal_name = STOPS[result.goal]["name"]

    print(f"--- {result.algorithm} ---")
    print(f"Looking for a route from {start_name} to {goal_name}.")

    if not result.found or not result.path:
        print("No path found.")
        return

    print(f"Nodes expanded (work done): {result.nodes_expanded}")
    print(f"Runtime: {result.runtime_seconds * 1000:.3f} ms")
    print(f"Hops: {result.hops}")
    print(f"Total travel time: {result.time_cost_minutes} min")
    print("Step-by-step:")

    path = result.path
    for i, stop_id in enumerate(path):
        name = STOPS[stop_id]["name"]
        if i == 0:
            print(f"  1. Start at {name}")
        elif i == len(path) - 1:
            leg = GRAPH[path[i - 1]][stop_id]
            print(f"  {i + 1}. Arrive at {name} (+{leg} min)  <-- goal")
        else:
            leg = GRAPH[path[i - 1]][stop_id]
            print(f"  {i + 1}. Go to {name} (+{leg} min)")

    if result.algorithm == "BFS":
        print(
            "Why this path? BFS prefers fewest hops "
            "(fewest stage changes), not necessarily fewest minutes."
        )
    elif result.algorithm == "DFS":
        print(
            "Why this path? DFS went deep along one branch first. "
            "It is not trying to be optimal."
        )
    elif result.algorithm == "A*":
        print(
            "Why this path? A* minimizes travel time, guided by "
            "straight-line distance toward the goal."
        )
    print()


def compare_plain_language(
    bfs_r: SearchResult,
    dfs_r: SearchResult,
    astar_r: SearchResult,
) -> None:
    print("=" * 70)
    print("DEMO SUMMARY")
    print("=" * 70)

    print(
        f"BFS found a {bfs_r.hops}-hop route taking {bfs_r.time_cost_minutes} min."
    )
    print(
        f"DFS found a {dfs_r.hops}-hop route taking {dfs_r.time_cost_minutes} min."
    )
    print(
        f"A* found a {astar_r.hops}-hop route taking {astar_r.time_cost_minutes} min."
    )
    print()

    times = {
        "BFS": bfs_r.time_cost_minutes,
        "DFS": dfs_r.time_cost_minutes,
        "A*": astar_r.time_cost_minutes,
    }
    best_algo = min(times, key=lambda k: times[k] if times[k] is not None else 10**9)
    print(
        f"Fastest travel time among these three: {best_algo} "
        f"({times[best_algo]} min)."
    )
    print(
        "For Nairobi matatu passengers who care about time, A* is usually "
        "the most suitable of the three."
    )
    print()


def run_demo(start: str, goal: str) -> None:
    start_name = STOPS[start]["name"]
    goal_name = STOPS[goal]["name"]

    print("=" * 70)
    print("INTELLIGENT PATH FINDER - LIVE DEMO")
    print("=" * 70)
    print(f"Request: {start_name} ({start}) -> {goal_name} ({goal})")
    print()

    bfs_r = bfs(start, goal)
    dfs_r = dfs(start, goal)
    astar_r = astar(start, goal)

    step_by_step(bfs_r)
    step_by_step(dfs_r)
    step_by_step(astar_r)
    compare_plain_language(bfs_r, dfs_r, astar_r)

    if astar_r.path:
        title = (
            f"A* route: {start_name} -> {goal_name} "
            f"({astar_r.time_cost_minutes} min)"
        )
        filename = plot_route(
            path=astar_r.path,
            title=title,
            filename="demo_route_map.png",
            show=False,
        )
        print(f"Route map saved as: {filename}")
        print("Red line = chosen A* path. Bright green ring = start. Bright blue ring = goal.")


if __name__ == "__main__":
    start_id, goal_id = parse_args(sys.argv)
    run_demo(start_id, goal_id)
