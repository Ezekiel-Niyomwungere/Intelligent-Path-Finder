"""
Phase 1 — Nairobi matatu network model.

This file does NOT search for routes yet.
It only stores:
  - stops (nodes)
  - coordinates (for A* later)
  - connections with travel times in minutes (edges)
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# 1. STOPS (nodes)
#    Each stop has a display name and approximate map coordinates.
# ---------------------------------------------------------------------------

StopInfo = Dict[str, float | str]

STOPS: Dict[str, StopInfo] = {
    "cbd": {"name": "CBD", "lat": -1.286, "lon": 36.817},
    "ngara": {"name": "Ngara", "lat": -1.274, "lon": 36.833},
    "parklands": {"name": "Parklands", "lat": -1.261, "lon": 36.818},
    "westlands": {"name": "Westlands", "lat": -1.268, "lon": 36.812},
    "kangemi": {"name": "Kangemi", "lat": -1.265, "lon": 36.752},
    "kawangware": {"name": "Kawangware", "lat": -1.284, "lon": 36.751},
    "junction": {"name": "The Junction", "lat": -1.298, "lon": 36.766},
    "karen": {"name": "Karen", "lat": -1.320, "lon": 36.702},
    "langata": {"name": "Lang'ata", "lat": -1.336, "lon": 36.777},
    "rongai": {"name": "Ong'ata Rongai", "lat": -1.396, "lon": 36.753},
    "south_b": {"name": "South B", "lat": -1.310, "lon": 36.838},
    "buruburu": {"name": "Buru Buru", "lat": -1.283, "lon": 36.878},
    "donholm": {"name": "Donholm", "lat": -1.293, "lon": 36.899},
    "embakasi": {"name": "Embakasi", "lat": -1.323, "lon": 36.895},
    "kasarani": {"name": "Kasarani", "lat": -1.222, "lon": 36.896},
}


# ---------------------------------------------------------------------------
# 2. RAW EDGES
#    Each tuple is: (stop_a, stop_b, time_minutes)
#    We treat routes as two-way, so we add both directions when building
#    the adjacency list below.
# ---------------------------------------------------------------------------

RawEdge = Tuple[str, str, int]

RAW_EDGES: List[RawEdge] = [
    # CBD hub
    ("cbd", "ngara", 10),
    ("cbd", "parklands", 18),
    ("cbd", "westlands", 15),
    ("cbd", "junction", 20),
    ("cbd", "south_b", 25),
    ("cbd", "buruburu", 30),
    # West
    ("westlands", "parklands", 10),
    ("westlands", "kangemi", 20),
    ("westlands", "kawangware", 25),
    ("kangemi", "kawangware", 15),
    ("kawangware", "junction", 25),
    # South / Southwest
    ("junction", "karen", 20),
    ("junction", "langata", 15),
    ("karen", "langata", 20),
    ("karen", "rongai", 25),
    ("langata", "rongai", 20),
    ("langata", "south_b", 15),
    # East
    ("south_b", "buruburu", 20),
    ("buruburu", "donholm", 15),
    ("donholm", "embakasi", 20),
    ("south_b", "embakasi", 25),
    # North
    ("ngara", "kasarani", 35),
    ("parklands", "kasarani", 30),
    ("buruburu", "kasarani", 40),
]


# ---------------------------------------------------------------------------
# 3. ADJACENCY LIST (the graph the search algorithms will use)
#
#    Shape:
#      {
#        "cbd": {"westlands": 15, "ngara": 10, ...},
#        "westlands": {"cbd": 15, "parklands": 10, ...},
#        ...
#      }
#
#    Meaning:
#      GRAPH["cbd"]["westlands"] == 15
#      → from CBD you can go to Westlands in 15 minutes
# ---------------------------------------------------------------------------

Graph = Dict[str, Dict[str, int]]


def build_graph(edges: List[RawEdge]) -> Graph:
    """Turn a list of undirected edges into a two-way adjacency list."""
    graph: Graph = {stop_id: {} for stop_id in STOPS}

    for a, b, minutes in edges:
        if a not in STOPS or b not in STOPS:
            raise ValueError(f"Unknown stop in edge: {a} -- {b}")
        if minutes <= 0:
            raise ValueError(f"Edge cost must be positive: {a} -- {b} ({minutes})")

        # Two-way: A→B and B→A with the same time
        graph[a][b] = minutes
        graph[b][a] = minutes

    return graph


GRAPH: Graph = build_graph(RAW_EDGES)


# ---------------------------------------------------------------------------
# 4. Helper functions (small tools we will reuse in later phases)
# ---------------------------------------------------------------------------

def neighbors(stop_id: str) -> Dict[str, int]:
    """Return {neighbor_id: minutes} for one stop."""
    return GRAPH[stop_id]


def travel_time(a: str, b: str) -> int | None:
    """Direct edge time from a to b, or None if not directly connected."""
    return GRAPH[a].get(b)


def straight_line_km(a: str, b: str) -> float:
    """
    Approximate crow-flies distance in kilometres.

    Near Nairobi (equator), 1 degree ≈ 111 km for both lat and lon.
    This is for A* later — not used for routing yet.
    """
    lat1 = float(STOPS[a]["lat"])
    lon1 = float(STOPS[a]["lon"])
    lat2 = float(STOPS[b]["lat"])
    lon2 = float(STOPS[b]["lon"])

    km_north = (lat2 - lat1) * 111.0
    km_east = (lon2 - lon1) * 111.0
    return math.sqrt(km_north**2 + km_east**2)


def summarize_network() -> None:
    """Print a short human-readable check that the model loaded correctly."""
    edge_count = sum(len(nbs) for nbs in GRAPH.values()) // 2

    print("=== Nairobi Matatu Network (Phase 1) ===")
    print(f"Stops (nodes): {len(STOPS)}")
    print(f"Routes (undirected edges): {edge_count}")
    print()
    print("Connections from CBD:")
    for dest, minutes in sorted(GRAPH["cbd"].items(), key=lambda item: item[1]):
        dest_name = STOPS[dest]["name"]
        print(f"  CBD -> {dest_name:15}  {minutes:2} min")
    print()
    print("Sample straight-line distances (for A* later):")
    print(f"  CBD -> Rongai    ~ {straight_line_km('cbd', 'rongai'):.1f} km")
    print(f"  CBD -> Embakasi  ~ {straight_line_km('cbd', 'embakasi'):.1f} km")
    print(f"  CBD -> Westlands ~ {straight_line_km('cbd', 'westlands'):.1f} km")


if __name__ == "__main__":
    summarize_network()
