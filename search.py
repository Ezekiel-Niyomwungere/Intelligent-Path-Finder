"""
Search algorithms for the Nairobi matatu network.

Uninformed:
  BFS — fewest hops (not necessarily fewest minutes)
  DFS — deep-first; any path, not guaranteed best

Informed:
  A* — uses a straight-line heuristic to aim for fewest minutes
"""

from __future__ import annotations

import heapq
import time
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional, Set, Tuple

from network import GRAPH, STOPS, straight_line_km


@dataclass
class SearchResult:
    """Everything we want to compare between algorithms later."""

    algorithm: str
    start: str
    goal: str
    path: Optional[List[str]]
    hops: Optional[int]
    time_cost_minutes: Optional[int]
    nodes_expanded: int
    runtime_seconds: float
    found: bool

    def explain(self) -> None:
        """Print a student-friendly summary of this search run."""
        start_name = STOPS[self.start]["name"]
        goal_name = STOPS[self.goal]["name"]

        print(f"=== {self.algorithm} ===")
        print(f"From: {start_name} ({self.start})")
        print(f"To:   {goal_name} ({self.goal})")
        print(f"Nodes expanded: {self.nodes_expanded}")
        print(f"Runtime: {self.runtime_seconds * 1000:.3f} ms")

        if not self.found or self.path is None:
            print("Result: no path found")
            return

        pretty = " -> ".join(STOPS[s]["name"] for s in self.path)
        print(f"Path: {pretty}")
        print(f"Hops (edges used): {self.hops}")
        print(f"Total travel time: {self.time_cost_minutes} min")

        if self.algorithm == "BFS":
            print(
                "Note: BFS optimizes hops (number of rides/segments), "
                "not necessarily minutes."
            )
        elif self.algorithm == "DFS":
            print(
                "Note: DFS does NOT optimize hops or minutes. "
                "It returns the first path it finds by going deep."
            )
        elif self.algorithm == "A*":
            print(
                "Note: A* aims for the lowest travel time (minutes), "
                "guided by a straight-line distance heuristic."
            )


def path_time_minutes(path: List[str]) -> int:
    """Sum edge times along an already-found path."""
    total = 0
    for a, b in zip(path, path[1:]):
        total += GRAPH[a][b]
    return total


def bfs(start: str, goal: str) -> SearchResult:
    """
    Breadth-First Search.

    Idea:
      - Use a queue (FIFO): first in, first out
      - Explore layer by layer: all 1-hop stops, then 2-hop, then 3-hop...
      - The first time we reach the goal, that path has the fewest hops

    We also track:
      - parent[stop] = previous stop (to rebuild the path)
      - nodes_expanded = how many stops we pulled from the queue
    """
    started_at = time.perf_counter()

    if start not in GRAPH or goal not in GRAPH:
        raise ValueError(f"Unknown stop id: {start!r} or {goal!r}")

    if start == goal:
        runtime = time.perf_counter() - started_at
        return SearchResult(
            algorithm="BFS",
            start=start,
            goal=goal,
            path=[start],
            hops=0,
            time_cost_minutes=0,
            nodes_expanded=0,
            runtime_seconds=runtime,
            found=True,
        )

    queue: Deque[str] = deque([start])
    visited: Set[str] = {start}
    parent: Dict[str, str] = {}
    nodes_expanded = 0

    found = False

    while queue:
        current = queue.popleft()
        nodes_expanded += 1

        # Look at every direct matatu neighbour
        for next_stop in GRAPH[current]:
            if next_stop in visited:
                continue

            visited.add(next_stop)
            parent[next_stop] = current
            queue.append(next_stop)

            if next_stop == goal:
                found = True
                # Clear the queue so the while-loop ends cleanly
                queue.clear()
                break

    runtime = time.perf_counter() - started_at

    if not found:
        return SearchResult(
            algorithm="BFS",
            start=start,
            goal=goal,
            path=None,
            hops=None,
            time_cost_minutes=None,
            nodes_expanded=nodes_expanded,
            runtime_seconds=runtime,
            found=False,
        )

    # Rebuild path: goal -> ... -> start, then reverse
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()

    return SearchResult(
        algorithm="BFS",
        start=start,
        goal=goal,
        path=path,
        hops=len(path) - 1,
        time_cost_minutes=path_time_minutes(path),
        nodes_expanded=nodes_expanded,
        runtime_seconds=runtime,
        found=True,
    )


def dfs(start: str, goal: str) -> SearchResult:
    """
    Depth-First Search.

    Idea:
      - Use a stack (LIFO): last in, first out
      - Dive deep along one branch before trying alternatives
      - First path found is NOT guaranteed to be shortest (hops or time)

    Contrast with BFS:
      - BFS queue = explore broadly, layer by layer
      - DFS stack = explore deeply, one corridor at a time
    """
    started_at = time.perf_counter()

    if start not in GRAPH or goal not in GRAPH:
        raise ValueError(f"Unknown stop id: {start!r} or {goal!r}")

    if start == goal:
        runtime = time.perf_counter() - started_at
        return SearchResult(
            algorithm="DFS",
            start=start,
            goal=goal,
            path=[start],
            hops=0,
            time_cost_minutes=0,
            nodes_expanded=0,
            runtime_seconds=runtime,
            found=True,
        )

    # Stack instead of queue — only structural difference from BFS
    stack: List[str] = [start]
    visited: Set[str] = {start}
    parent: Dict[str, str] = {}
    nodes_expanded = 0

    found = False

    while stack:
        current = stack.pop()  # LIFO: take the newest stop
        nodes_expanded += 1

        for next_stop in GRAPH[current]:
            if next_stop in visited:
                continue

            visited.add(next_stop)
            parent[next_stop] = current
            stack.append(next_stop)

            if next_stop == goal:
                found = True
                stack.clear()
                break

    runtime = time.perf_counter() - started_at

    if not found:
        return SearchResult(
            algorithm="DFS",
            start=start,
            goal=goal,
            path=None,
            hops=None,
            time_cost_minutes=None,
            nodes_expanded=nodes_expanded,
            runtime_seconds=runtime,
            found=False,
        )

    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()

    return SearchResult(
        algorithm="DFS",
        start=start,
        goal=goal,
        path=path,
        hops=len(path) - 1,
        time_cost_minutes=path_time_minutes(path),
        nodes_expanded=nodes_expanded,
        runtime_seconds=runtime,
        found=True,
    )


# ---------------------------------------------------------------------------
# Phase 3 — Informed search: A*
# ---------------------------------------------------------------------------

def max_edge_speed_kmh() -> float:
    """
    Fastest implied speed on any edge (km/h).

    We use this as v_max so the heuristic never assumes we can go faster
    than any real edge in our model → keeps h admissible.
    """
    best = 0.0
    for a, nbs in GRAPH.items():
        for b, minutes in nbs.items():
            if a >= b:
                continue  # each undirected edge once
            km = straight_line_km(a, b)
            speed = km / (minutes / 60.0)
            if speed > best:
                best = speed
    return best


# Computed once from our network (~29.4 km/h on Lang'ata--South B)
MAX_SPEED_KMH: float = max_edge_speed_kmh()


def heuristic_minutes(stop_id: str, goal: str) -> float:
    """
    h(n): estimated remaining travel time in minutes.

    straight-line km / v_max * 60

    This is a LOWER BOUND on true remaining time (admissible), because:
      1) real routes are at least as long as crow-flies distance
      2) we never assume a speed faster than our fastest edge
    """
    km = straight_line_km(stop_id, goal)
    return (km / MAX_SPEED_KMH) * 60.0


def astar(start: str, goal: str) -> SearchResult:
    """
    A* search (informed).

    Scores for each stop n:
      g(n) = time so far from start to n  (known, from edges)
      h(n) = heuristic guess from n to goal (straight-line → minutes)
      f(n) = g(n) + h(n)  → estimated total journey time via n

    Always expand the stop with the smallest f first (priority queue).
    With an admissible heuristic, the first time we expand the goal,
    we have an optimal (lowest-minute) path.
    """
    started_at = time.perf_counter()

    if start not in GRAPH or goal not in GRAPH:
        raise ValueError(f"Unknown stop id: {start!r} or {goal!r}")

    if start == goal:
        runtime = time.perf_counter() - started_at
        return SearchResult(
            algorithm="A*",
            start=start,
            goal=goal,
            path=[start],
            hops=0,
            time_cost_minutes=0,
            nodes_expanded=0,
            runtime_seconds=runtime,
            found=True,
        )

    # Priority queue entries: (f_score, tie_breaker, stop_id)
    tie = 0
    open_heap: List[Tuple[float, int, str]] = []
    heapq.heappush(open_heap, (heuristic_minutes(start, goal), tie, start))

    g_score: Dict[str, float] = {start: 0.0}
    parent: Dict[str, str] = {}
    closed: Set[str] = set()
    nodes_expanded = 0
    found = False

    while open_heap:
        _f, _tie, current = heapq.heappop(open_heap)

        if current in closed:
            continue

        nodes_expanded += 1

        if current == goal:
            found = True
            break

        closed.add(current)

        for next_stop, edge_minutes in GRAPH[current].items():
            if next_stop in closed:
                continue

            tentative_g = g_score[current] + edge_minutes

            # Only update if this path to next_stop is better (or first time)
            if tentative_g < g_score.get(next_stop, float("inf")):
                g_score[next_stop] = tentative_g
                parent[next_stop] = current
                f_score = tentative_g + heuristic_minutes(next_stop, goal)
                tie += 1
                heapq.heappush(open_heap, (f_score, tie, next_stop))

    runtime = time.perf_counter() - started_at

    if not found:
        return SearchResult(
            algorithm="A*",
            start=start,
            goal=goal,
            path=None,
            hops=None,
            time_cost_minutes=None,
            nodes_expanded=nodes_expanded,
            runtime_seconds=runtime,
            found=False,
        )

    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()

    return SearchResult(
        algorithm="A*",
        start=start,
        goal=goal,
        path=path,
        hops=len(path) - 1,
        time_cost_minutes=path_time_minutes(path),
        nodes_expanded=nodes_expanded,
        runtime_seconds=runtime,
        found=True,
    )


if __name__ == "__main__":
    print("Comparing BFS, DFS, and A* on CBD -> Rongai\n")
    print(
        f"A* heuristic uses v_max = {MAX_SPEED_KMH:.1f} km/h "
        f"(fastest edge in our model)\n"
    )
    print(
        f"h(CBD -> Rongai) lower-bound guess: "
        f"{heuristic_minutes('cbd', 'rongai'):.1f} min "
        f"(true best path will be >= this)\n"
    )

    bfs("cbd", "rongai").explain()
    print()
    dfs("cbd", "rongai").explain()
    print()
    astar("cbd", "rongai").explain()
