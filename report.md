# Intelligent Path Finder for Nairobi Matatu Routes

**Course:** DSA2020 UB AI  
**Project focus:** Uninformed and informed search on a simplified Nairobi matatu network

---

## 1. Introduction

Nairobi’s public transport is dominated by matatus. Passengers routinely ask:

> “How do I get from A to B, and which option is better?”

This project models that question as a **graph search** problem:

- **Nodes** = matatu stages / stops  
- **Edges** = direct matatu links  
- **Edge cost** = estimated travel time in minutes

We implemented three classic search algorithms:

| Algorithm | Type | What it optimizes |
|-----------|------|-------------------|
| BFS | Uninformed | Fewest hops (stage changes) |
| DFS | Uninformed | No guarantee (first deep path) |
| A* | Informed | Lowest travel time (with a heuristic) |

The goal is not only to find routes, but to **compare efficiency** (path quality, nodes expanded, runtime) and discuss how well these methods fit **real Kenyan urban mobility**, where traffic is highly variable.

---

## 2. Problem modelling

### 2.1 Network design

We built a simplified Nairobi network with **15 stops** and **24 undirected routes**, covering:

- Centre: CBD, Ngara  
- West: Westlands, Parklands, Kangemi, Kawangware  
- East: Buru Buru, Donholm, Embakasi  
- North-East: Kasarani  

Each edge has a **static average travel time** (minutes). These times are teaching estimates for the assignment, not live GPS measurements.

### 2.2 Coordinates and heuristic support

Each stop also has approximate **latitude/longitude**.  
A* uses **straight-line (crow-flies) distance** converted into an estimated remaining time:

\[
h(n) = \frac{\text{straight-line km}(n,\text{goal})}{v_{\max}} \times 60
\]

where \(v_{\max}\) is the fastest speed implied by any edge in our model (~29.4 km/h).  
This keeps the heuristic **admissible** (it does not overestimate remaining time), so A* can return an optimal time path for this model.

### 2.3 What “hops” means

A **hop** is one stop-to-stop link on the path.  
Example: `CBD → Junction → Lang'ata → Rongai` has **3 hops** and **55 minutes**.

Hops ≠ minutes. That distinction is central to why BFS and A* disagree.

---

## 3. Algorithms

### 3.1 BFS (Breadth-First Search)

- Uses a **queue** (FIFO)  
- Explores layer by layer (1 hop, then 2 hops, …)  
- First path to the goal has the **fewest hops**  
- Does **not** minimize travel time when edges have different costs  

**Matatu interpretation:** useful if the passenger mainly wants **fewer stage changes / transfers**.

### 3.2 DFS (Depth-First Search)

- Uses a **stack** (LIFO)  
- Goes deep along one branch before backtracking  
- Finds *a* path, but quality is **unpredictable**  

**Matatu interpretation:** poor as a primary trip planner; good mainly as a contrast algorithm in learning/experiments.

### 3.3 A* (A-star)

- Uses a **priority queue** ordered by \(f(n) = g(n) + h(n)\)  
  - \(g(n)\): minutes already spent from start  
  - \(h(n)\): heuristic guess of minutes still needed to reach the destination 
- With an admissible heuristic, A* finds a **lowest-minute** path  

**Matatu interpretation:** closest of the three to what most passengers want: **get there in less time**.

---

## 4. Experimental comparison

We compared BFS, DFS, and A* on multiple start–goal pairs (for example CBD→Rongai, CBD→Embakasi, Westlands→Rongai, Kasarani→Karen, Kangemi→Donholm, Parklands→Embakasi).

Metrics:

1. Path travel time (minutes)  
2. Hops  
3. Nodes expanded  
4. Runtime  

Supporting outputs:

- Text comparison tables (`compare.py`)  
- Charts: travel time, nodes expanded, runtime  
- Interactive demo with map (`demo.py`, `demo_route_map.png`)

### 4.1 Example: CBD → Ong'ata Rongai

| Algorithm | Path | Hops | Time | Nodes expanded |
|-----------|------|------|------|----------------|
| BFS | CBD → Junction → Karen → Rongai | 3 | 65 min | 11 |
| DFS | CBD → South B → Lang'ata → Rongai | 3 | 60 min | 7 |
| A* | CBD → Junction → Lang'ata → Rongai | 3 | **55 min** | 8 |

All three used 3 hops, but **times differed**.  
A* recovered the best time path predicted during network design (`20 + 15 + 20 = 55`).

### 4.2 Broader pattern from the tests

- **BFS** consistently returns fewest (or tied) hops.  
- **A*** consistently returns lowest (or tied) travel time.  
- **DFS** is inconsistent: sometimes acceptable, sometimes clearly worse (more hops and more minutes).  
- On a **15-node** graph, runtime differences are tiny. A*’s practical advantage in search effort becomes clearer on **larger** networks.

---

## 5. Suitability for Kenyan traffic variability

### 5.1 What our model assumes

Our edge times are **static**:

- one fixed minute value per link  
- same cost in both directions  
- no peak vs off-peak difference  
- no rain, accidents, police checks, or stage congestion  

That is acceptable for learning search algorithms, but it is **not** how Nairobi traffic behaves day to day.

### 5.2 Real Nairobi factors the model misses

| Real-world factor | Effect on routing | Impact on algorithms |
|-------------------|-------------------|----------------------|
| Peak-hour jams (e.g. Waiyaki Way, Mombasa Rd, Ngong Rd) | Same “distance” can take much longer | Static A* may recommend a route that is slow today |
| Stage waiting / filling time | Delay before the matatu leaves | Not in edge costs; can dominate short hops |
| Route variability / diversion | Edges appear/disappear | Graph itself becomes outdated |
| One-way behaviour / unequal directions | A→B ≠ B→A in time | Our undirected equal costs oversimplify |
| Transfers and walking between stages | Extra time and uncertainty | Hop count alone understates passenger pain |
| Fare differences | Cheaper ≠ faster | Multi-criteria needed (time + money) |

### 5.3 Algorithm suitability under variability

**BFS**  
- Strength: stable notion of “few transfers.”  
- Weakness: ignores time; in traffic, a 2-hop jammed corridor can be worse than a 3-hop free-flow alternative.  
- Suitability in Kenya: useful as a **transfer-minimizing** option, not as a sole fastest-path engine.

**DFS**  
- Strength: simple to implement; can find some path quickly.  
- Weakness: no optimality; path quality depends on neighbour order.  
- Suitability in Kenya: **not recommended** for passenger-facing routing.

**A\***  
- Strength: principled for lowest-time routing when costs are trustworthy.  
- Weakness: “optimal” only for the **modelled costs**. If minutes are stale, the route can be optimally wrong for today’s traffic.  
- Suitability in Kenya: **best of the three** as a base method, provided edge weights are updated (or estimated) from current conditions.

### 5.4 Key report insight

> Search algorithm quality and data quality are inseparable.  
> In Nairobi, an excellent algorithm on outdated travel times can still give a bad journey.

So A* is the right *algorithmic* direction for time-based routing, but a production matatu navigator also needs **fresh costs** (and preferably uncertainty-aware planning).

---

## 6. Demo and deliverables

| Deliverable | How to run / find it |
|-------------|----------------------|
| Network model | `network.py` |
| BFS, DFS, A* | `search.py` |
| Comparison tables + charts | `python compare.py` |
| Live demo + explanations | `python demo.py cbd rongai` |
| Streamlit web interface | `streamlit run app.py` |
| Route map | `demo_route_map.png` |
| Comparison graphs | `comparison_travel_time.png`, `comparison_nodes_expanded.png`, `comparison_runtime.png` |

Demo behaviour:

1. User picks start and goal stops.  
2. System runs BFS, DFS, and A*.  
3. Each route is explained step-by-step.  
4. A* path is plotted on the map.  
5. Summary states which option is fastest in the model.

---

## 7. Limitations

1. Only 15 stops — real Nairobi has far more stages and informal alighting points.  
2. Travel times are estimated averages, not measured.  
3. No fares, waiting time, walking time, or comfort/safety factors.  
4. Undirected edges ignore asymmetric congestion.  
5. Heuristic assumes a maximum speed derived from the static model.  

---

## 8. Future improvements

1. **Dynamic edge weights** from traffic APIs, historical averages by time-of-day, or crowd reports.  
2. **Waiting-time model** at stages (often more painful than in-vehicle time).  
3. **Transfer-aware costs** (penalize changing matatus).  
4. **Multi-criteria routing** (time + fare + walking).  
5. Larger graph (more estates, satellites like Kitengela, Ruiru, Kikuyu).  
6. Uncertainty: recommend robust routes that stay decent if one corridor jams.

---

## 9. Conclusion

This project shows that Nairobi matatu routing can be represented as a weighted graph and solved with classic AI search:

- **BFS** is best for fewest stage changes.  
- **DFS** is unreliable for quality routes.  
- **A\*** is best for lowest travel time in a static model and is the most suitable of the three for passenger-oriented journey planning.

However, Kenyan urban mobility is defined by **traffic variability**. Algorithm choice matters, but so does keeping travel-time data realistic. The natural next step beyond this coursework prototype is an A*-style planner fed by **time-dependent, data-driven edge costs**.

---

## Appendix A — How to reproduce results

```bash
python network.py          # sanity-check the graph
python search.py           # quick BFS/DFS/A* printout
python compare.py          # full comparison + charts
python demo.py cbd rongai  # explained demo + map
streamlit run app.py       # Streamlit web UI
```

## Appendix B — Stop ids used in code

`cbd`, `ngara`, `parklands`, `westlands`, `kangemi`, `kawangware`, `junction`, `karen`, `langata`, `rongai`, `south_b`, `buruburu`, `donholm`, `embakasi`, `kasarani`
