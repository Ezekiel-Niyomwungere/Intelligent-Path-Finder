"""
Phase 5 — Visualize the matatu network and a chosen route.

Stops are plotted using longitude (x) and latitude (y).
All routes are drawn lightly; the selected path is highlighted.
"""

from __future__ import annotations

from typing import List, Optional

import matplotlib.pyplot as plt

from network import RAW_EDGES, STOPS


def plot_route(
    path: Optional[List[str]] = None,
    title: str = "Nairobi Matatu Network",
    filename: str = "route_map.png",
    show: bool = False,
) -> str:
    """
    Draw the full network. If path is given, highlight that route.

    Returns the filename that was saved.
    """
    fig, ax = plt.subplots(figsize=(10, 9))

    # 1) All edges (background network)
    for a, b, _minutes in RAW_EDGES:
        lon_a = float(STOPS[a]["lon"])
        lat_a = float(STOPS[a]["lat"])
        lon_b = float(STOPS[b]["lon"])
        lat_b = float(STOPS[b]["lat"])
        ax.plot(
            [lon_a, lon_b],
            [lat_a, lat_b],
            color="#c5c5c5",
            linewidth=1.2,
            zorder=1,
        )

    # 2) Highlight chosen path
    if path and len(path) >= 2:
        for a, b in zip(path, path[1:]):
            ax.plot(
                [float(STOPS[a]["lon"]), float(STOPS[b]["lon"])],
                [float(STOPS[a]["lat"]), float(STOPS[b]["lat"])],
                color="#c0392b",
                linewidth=3.5,
                zorder=3,
            )

    # 3) Stops
    path_set = set(path or [])
    for stop_id, info in STOPS.items():
        lon = float(info["lon"])
        lat = float(info["lat"])
        on_path = stop_id in path_set

        ax.scatter(
            lon,
            lat,
            s=90 if on_path else 55,
            color="#c0392b" if on_path else "#2c3e50",
            zorder=4,
            edgecolors="white",
            linewidths=0.8,
        )
        ax.annotate(
            str(info["name"]),
            (lon, lat),
            textcoords="offset points",
            xytext=(6, 6),
            fontsize=8,
            color="#1a1a1a",
        )

    # 4) Mark start / goal with clearly different colours
    if path:
        start, goal = path[0], path[-1]
        ax.scatter(
            float(STOPS[start]["lon"]),
            float(STOPS[start]["lat"]),
            s=220,
            facecolors="none",
            edgecolors="#00C853",  # bright green = start
            linewidths=3.5,
            zorder=5,
            label="Start",
        )
        ax.scatter(
            float(STOPS[goal]["lon"]),
            float(STOPS[goal]["lat"]),
            s=220,
            facecolors="none",
            edgecolors="#0088FF",  # bright blue = goal
            linewidths=3.5,
            zorder=5,
            label="Goal",
        )
        ax.legend(loc="lower left")

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(title)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.set_aspect("equal", adjustable="datalim")
    fig.tight_layout()
    fig.savefig(filename, dpi=140)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return filename
