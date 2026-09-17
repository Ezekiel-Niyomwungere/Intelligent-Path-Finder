# Presentation slides

**Intelligent Path Finder for Nairobi Matatu Routes**

Uninformed & Informed Search for Urban Mobility

- Course: DSA2020 UB AI  
- Focus: Graph search on a simplified matatu network

---

## Slide 2 - Problem statement

**Problem**

- Matatus dominate Nairobi public transport  
- Passengers need routes from A → B  
- “Better” can mean fewer changes **or** less time  

**This project**

- Model routes as a **graph search** problem  
- Compare **BFS**, **DFS**, and **A\***  
- Link results to **real Kenyan traffic** challenges  

---

## Slide 3 - Objectives

**What we set out to do**

1. Model a simplified Nairobi matatu network (15 stops)  
2. Implement BFS, DFS, and A*  
3. Compare: path time, hops, nodes expanded, runtime  
4. Visualize & demo routes  
5. Discuss algorithm fit for traffic variability  

---

## Slide 4 - Network model

**Graph design**

| Element | Meaning |
|--------|---------|
| Node | Matatu stop / stage |
| Edge | Direct matatu link |
| Cost | Travel time (minutes) |

**Scale**

- **15** stops (CBD, Westlands, Rongai, Embakasi, …)  
- **24** undirected routes  
- Coordinates for A* straight-line heuristic  

*Note: times are static estimates, not live GPS.*

---

## Slide 5 - Algorithms (overview)

| Algorithm | Type | Optimizes |
|-----------|------|-----------|
| **BFS** | Uninformed | Fewest **hops** |
| **DFS** | Uninformed | *No guarantee* |
| **A\*** | Informed | Lowest **minutes** |

**Key idea**

- Hop = one stop → next stop  
- Hops ≠ minutes  

---

## Slide 6 - How the algorithms work

**BFS** — queue (layer by layer) → fewest stage changes  

**DFS** — stack (go deep first) → any path, quality unreliable  

**A\*** — priority by  
`f = g + h`

- **g** = minutes so far  
- **h** = straight-line time guess to goal  
- Admissible **h** → optimal time (for this model)  

---

## Slide 7 - Results (example)

**CBD → Ong'ata Rongai**

| Algo | Hops | Time |
|------|------|------|
| BFS | 3 | 65 min |
| DFS | 3 | 60 min |
| **A\*** | 3 | **55 min** |

Same hops, **different times** → A* finds the fastest route in the model.

---

## Slide 8 - Key findings

- **BFS** → best / tied on hops  
- **A\*** → best / tied on travel time  
- **DFS** → inconsistent (sometimes much worse)  
- On 15 nodes, runtimes are all tiny  
- A* scales better on **larger** networks  

---

## Slide 9 - Kenya context & limitations

**Real traffic vs our model**

| Real world | Our model |
|------------|-----------|
| Peak jams, diversions | Fixed edge times |
| Stage waiting | Not included |
| A→B ≠ B→A | Undirected equal costs |

**Insight**

> Algorithm quality **and** data quality both matter.  
> Good A* + stale times = still a bad trip.

**Limits:** 15 stops · estimated times · no fares / waiting  

---

## Slide 10 - Conclusion & future work

**Conclusion**

- Matatu routing works as weighted graph search  
- **A\*** best for time-based routing (of the three)  
- **BFS** useful for fewer transfers  
- **DFS** not for passenger apps  

**Next steps**

- Live / time-of-day travel times  
- Waiting & transfer costs  
- Larger network + multi-criteria (time + fare)  
