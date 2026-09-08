"""
Intelligent Path Finder — Streamlit web app.
"""

from __future__ import annotations

import os
import tempfile
from typing import Dict

import streamlit as st

from network import STOPS
from search import SearchResult, astar, bfs, dfs
from visualize import plot_route


st.set_page_config(
    page_title="Intelligent Path Finder",
    layout="wide",
)

STOP_OPTIONS = {str(info["name"]): sid for sid, info in STOPS.items()}

def result_to_dict(result: SearchResult) -> Dict:
    """Turn a SearchResult into display-friendly fields."""
    notes = {
        "BFS": "Fewest hops (stage changes). Not always fewest minutes.",
        "DFS": "First deep path found. Not trying to be optimal.",
        "A*": "Lowest travel time, guided by straight-line distance.",
    }

    if not result.found or not result.path:
        return {
            "algorithm": result.algorithm,
            "found": False,
            "path_names": [],
            "hops": None,
            "minutes": None,
            "expanded": result.nodes_expanded,
            "runtime_ms": round(result.runtime_seconds * 1000, 3),
            "note": "No path found.",
        }

    return {
        "algorithm": result.algorithm,
        "found": True,
        "path_names": [str(STOPS[s]["name"]) for s in result.path],
        "path_ids": result.path,
        "hops": result.hops,
        "minutes": result.time_cost_minutes,
        "expanded": result.nodes_expanded,
        "runtime_ms": round(result.runtime_seconds * 1000, 3),
        "note": notes.get(result.algorithm, ""),
    }


def render_result_card(data: Dict) -> None:
    st.subheader(data["algorithm"])
    if not data["found"]:
        st.write("No path found.")
        return

    st.markdown(f"**Hops:** {data['hops']}")
    st.markdown(f"**Travel time:** {data['minutes']} min")
    st.markdown(f"**Nodes expanded:** {data['expanded']}")
    st.markdown(f"**Runtime:** {data['runtime_ms']} ms")
    st.info(" → ".join(data["path_names"]))
    st.caption(data["note"])


st.title("Intelligent Path Finder")
st.markdown(
    "Nairobi matatu routes — pick where you are and where you want to go. "
    "Compare **BFS**, **DFS**, and **A\\*** without touching the code."
)

names = list(STOP_OPTIONS.keys())
default_start = names.index("CBD") if "CBD" in names else 0
default_goal = names.index("Ong'ata Rongai") if "Ong'ata Rongai" in names else 1

col_a, col_b, col_c = st.columns([2, 2, 1])
with col_a:
    start_name = st.selectbox("Starting place", names, index=default_start)
with col_b:
    goal_name = st.selectbox("Destination", names, index=default_goal)
with col_c:
    st.write("")
    st.write("")
    find = st.button("Find routes", type="primary", use_container_width=True)

start = STOP_OPTIONS[start_name]
goal = STOP_OPTIONS[goal_name]

if find:
    if start == goal:
        st.error("Start and destination are the same. Pick two different places.")
    else:
        bfs_r = bfs(start, goal)
        dfs_r = dfs(start, goal)
        astar_r = astar(start, goal)

        results = [
            result_to_dict(bfs_r),
            result_to_dict(dfs_r),
            result_to_dict(astar_r),
        ]

        times = {
            "BFS": bfs_r.time_cost_minutes,
            "DFS": dfs_r.time_cost_minutes,
            "A*": astar_r.time_cost_minutes,
        }
        best = min(
            times,
            key=lambda k: times[k] if times[k] is not None else 10**9,
        )

        st.success(
            f"From **{start_name}** to **{goal_name}**: fastest among these three is "
            f"**{best}** ({times[best]} min)."
        )

        c1, c2, c3 = st.columns(3)
        for col, data in zip((c1, c2, c3), results):
            with col:
                render_result_card(data)

        if astar_r.path:
            st.markdown("---")
            st.subheader("A* route map")
            st.caption(
                "Red line = chosen A* path. Bright green ring = start. "
                "Bright blue ring = goal."
            )

            map_path = os.path.join(tempfile.gettempdir(), "ipf_route_map.png")
            plot_route(
                path=astar_r.path,
                title=(
                    f"A* route: {start_name} -> {goal_name} "
                    f"({astar_r.time_cost_minutes} min)"
                ),
                filename=map_path,
                show=False,
            )
            st.image(map_path, use_container_width=True)

st.markdown("---")
st.caption(
    "Local Streamlit app. Run with `streamlit run app.py`. "
)
