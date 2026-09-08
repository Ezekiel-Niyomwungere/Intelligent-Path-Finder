# Intelligent Path Finder for Nairobi Matatu Routes

A graph-search project that finds matatu routes across a simplified Nairobi network using **BFS**, **DFS**, and **A\***, then compares how each algorithm performs on path quality and search cost.

Built for **DSA2020 UB AI** — applying uninformed and informed search to a real-world Kenyan urban mobility problem.

---

## Overview

Nairobi passengers often need to get from one place to another by matatu. This project treats that problem as classic AI search:

| Concept | In this project |
|---------|-----------------|
| **Node** | Matatu stage / stop |
| **Edge** | Direct matatu link between two stops |
| **Cost** | Estimated travel time (minutes) |
| **Path** | Sequence of stops from origin to destination |

The system implements three algorithms, compares them fairly, visualizes routes, and exposes results through a local web demo.

---

## Features

- **15 Nairobi stops** and **24 undirected routes** (CBD, Westlands, Ong'ata Rongai, Embakasi, Kasarani, …)
- **BFS** — fewest hops (stage changes)
- **DFS** — deep-first pathfinding (not optimal)
- **A\*** — lowest travel time with a straight-line distance heuristic
- Side-by-side **comparison tables and charts**
- **Terminal demo** with step-by-step explanations
- **Streamlit web app** — pick start/destination in the browser
- Full **project report** discussing traffic variability in Kenya

---

## Project structure

```text
AI Project/
├── network.py              # Stops, edges, coordinates, graph helpers
├── search.py               # BFS, DFS, A*, SearchResult metrics
├── compare.py              # Batch comparison + matplotlib charts
├── visualize.py            # Route map plotting
├── demo.py                 # CLI demo with explanations
├── app.py                  # Streamlit web interface
├── report.md               # Full technical report
├── presentation_slides.md  # 10-slide presentation outline
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

Generated when you run tools (optional to commit):

```text
comparison_travel_time.png
comparison_nodes_expanded.png
comparison_runtime.png
demo_route_map.png
static/route_map.png        # produced by the web app
```

---

## Requirements

- **Python 3.10+** (tested with Python 3.13)
- Packages listed in `requirements.txt`:

```text
streamlit
matplotlib
```

### Install

```bash
cd "path/to/AI Project"
pip install -r requirements.txt
```

---

## Quick start

### 1. Check the network model

```bash
python network.py
```

Prints stop count, routes from CBD, and sample straight-line distances.

### 2. Run search algorithms (terminal)

```bash
python search.py
```

Compares BFS, DFS, and A* on **CBD → Ong'ata Rongai** by default.  
Edit the bottom of `search.py` to try other stop IDs.

### 3. Full algorithm comparison + charts

```bash
python compare.py
```

Runs several start–goal pairs and saves:

- `comparison_travel_time.png`
- `comparison_nodes_expanded.png`
- `comparison_runtime.png`

### 4. CLI demo with explanations

```bash
python demo.py cbd rongai
python demo.py westlands embakasi
```

### 5. Web interface (Streamlit)

```bash
streamlit run app.py
```

Streamlit will open a browser tab (usually **http://localhost:8501**).

1. Choose **Starting place**
2. Choose **Destination**
3. Click **Find routes**

You get BFS / DFS / A* results plus an A* route map.

> **Note:** Locally, `localhost` only works on the machine running the app.  
> For a public link later, you can deploy the same `app.py` to [Streamlit Community Cloud](https://streamlit.io/cloud).

---

## Available stops

| ID | Display name |
|----|----------------|
| `cbd` | CBD |
| `ngara` | Ngara |
| `parklands` | Parklands |
| `westlands` | Westlands |
| `kangemi` | Kangemi |
| `kawangware` | Kawangware |
| `junction` | The Junction |
| `karen` | Karen |
| `langata` | Lang'ata |
| `rongai` | Ong'ata Rongai |
| `south_b` | South B |
| `buruburu` | Buru Buru |
| `donholm` | Donholm |
| `embakasi` | Embakasi |
| `kasarani` | Kasarani |

---

## Algorithms (short guide)

### BFS (Breadth-First Search)

- Structure: **queue** (FIFO)
- Explores layer by layer
- First path found has the **fewest hops**
- Does **not** guarantee lowest travel time when edges have different costs

**Useful when:** the passenger mainly wants fewer stage changes.

### DFS (Depth-First Search)

- Structure: **stack** (LIFO)
- Goes deep along one branch first
- Finds *a* path; quality is **unpredictable**

**Useful when:** learning / contrast experiments — not for passenger-facing routing.

### A* (A-star)

- Structure: **priority queue** ordered by  
  \(f(n) = g(n) + h(n)\)
  - \(g(n)\): minutes already spent from the start  
  - \(h(n)\): estimated remaining time from straight-line distance  
- With an **admissible** heuristic, A* returns a **lowest-minute** path for this model

**Useful when:** optimizing travel time (closest of the three to real trip planning).

### Hops vs minutes

A **hop** is one stop-to-stop link.  
Example: `CBD → Junction → Lang'ata → Rongai` = **3 hops**, **55 minutes**.

Same hop count can still mean different travel times — that is why BFS and A* often disagree.

---

## Example result

**CBD → Ong'ata Rongai**

| Algorithm | Path (summary) | Hops | Time |
|-----------|----------------|------|------|
| BFS | CBD → Junction → Karen → Rongai | 3 | 65 min |
| DFS | CBD → South B → Lang'ata → Rongai | 3 | 60 min |
| **A\*** | CBD → Junction → Lang'ata → Rongai | 3 | **55 min** |

All three use 3 hops; **A\*** recovers the fastest route under the model costs (`20 + 15 + 20 = 55`).

### Broader comparison pattern

- **BFS** → best or tied on hops  
- **A\*** → best or tied on travel time  
- **DFS** → inconsistent; sometimes clearly worse  
- On a small (15-node) graph, runtimes are all tiny  

---

## Model assumptions and limitations

Travel times in this project are **static teaching estimates**, not live traffic data.

Not modelled yet:

- Peak-hour congestion vs off-peak
- Stage waiting / filling time
- Route diversions
- One-way or asymmetric travel times
- Fares, walking, comfort, safety

**Key report insight:** algorithm quality and data quality go together. A perfect search on stale minutes can still produce a bad Nairobi trip.

---

## Future work

- Dynamic / time-of-day edge weights  
- Stage waiting-time model  
- Transfer penalties  
- Multi-criteria routing (time + fare + walking)  
- Larger network (more estates and satellite towns)  

---

## Documentation in this repo

| File | Purpose |
|------|---------|
| [report.md](report.md) | Full technical write-up (methods, results, Kenya context) |
| [presentation_slides.md](presentation_slides.md) | 10-slide presentation outline |

---

## How to present this project

1. Open `presentation_slides.md` for talking points.  
2. Live demo: `streamlit run app.py` → browser.  
3. Optional: show comparison charts from `python compare.py`.  

Suggested spoken line for “local deploy”:

> “The app runs on my laptop with Streamlit. Opening `http://localhost:8501` talks to this machine only until we deploy it to Streamlit Cloud.”

---

## License

Academic / educational project. You may adapt the code for learning and coursework with attribution.

---

## Author

Built as a **DSA2020 UB AI** project applying search algorithms to Nairobi matatu routing.

---

## Acknowledgements

- Course focus on uninformed and informed search  
- Simplified Nairobi geography for a clean teaching graph (not official transit GTFS data)
