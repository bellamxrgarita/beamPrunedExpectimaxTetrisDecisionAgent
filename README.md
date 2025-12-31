# Project Overview 
This project explores how to design scalable, autonomous decision-making agents for Tetris, a stochastic game with exponential state-space growth that makes optimal planning computationally intractable. The goal was to build an agent that maximizes the number of lines cleared while maintaining long-term board stability, rather than simply optimizing short-term moves.

Tetris is challenging because each piece placement dramatically increases the number of possible future board configurations. While the next two pieces are known, all subsequent pieces are generated randomly, causing naïve search strategies to become unusable due to exponential branching. This project focuses on identifying those limitations and redesigning the decision process to operate effectively under real computational constraints.



## Requirements
- Python 3.9+
- Tkinter (bundled with standard Python installations)
> Note: Tkinter is included with most Python distributions. If you encounter an
> import error, ensure that Python was installed with Tk support.

# How to Run and Test the Agents

1. How to Visualize Agent Decisions
Use gameSimulator.py to watch an agent play Tetris and observe its decision-making process in real time. 
```
python3 gameSimulator.py <agent>
```
Supported Agents Arguments:
- expectimax
- beamSearchChance
- beamPrunedExpectimax 

Example:
```
python3 gameSimulator.py beamSearchChance
```
This launches a GUI simulation (via Tkinter) that visualizes the agent’s piece placements, line clears, and board evolution.

2. Run Quantative Benchmarks (Agent Simulator)
Use agentSimulator.py to run headless simulations and compare agent performance at scale of the two beamsearch agent hybrids. 
```
python3 agentSimulator.py
```
This script automatically:
- Simulates multiple runs for each supported agent

- Limits the number of pieces per run

- Records metrics such as:

- Total pieces placed

- Total lines cleared

- Average lines cleared per piece (decision quality)

The benchmark is designed to compare decision quality over long horizons, not just short-term survival.

## Approach 
The system is built around a compact, abstract state-space representation that collapses real-time game mechanics (movement, gravity, rotation) into a single discrete action: placing a piece at a chosen column and orientation. This abstraction drastically reduces the size of the state space and enables tractable search over future game states.

Three agents were implemented and evaluated:

Baseline Expectimax: A depth-limited Expectimax agent that explicitly models stochastic future pieces. While theoretically sound, this approach quickly became impractical due to exponential branching.

Beam Search with Chance Layer: A hybrid agent that prunes low-utility intermediate states using heuristic evaluation while still accounting for randomness at the leaf level.

Beam-Pruned Expectimax (Final Agent): A refined hybrid that combines Expectimax’s stochastic modeling with beam pruning to improve both runtime performance and long-horizon decision quality.

All agents rely on a heuristic evaluation function inspired by Pierre Dellacherie’s seminal Tetris algorithm, which is widely regarded as one of the most effective one-piece Tetris strategies ever developed. The heuristic evaluates board states using features such as aggregate column height, number of holes, surface roughness (bumpiness), and lines cleared, encouraging low-risk, stable board configurations that support sustained play.

## System Design 
The project is modularized into:

A Tetris state-space class that exposes legal placements and abstract state transitions

Multiple decision agents implementing different search strategies

A game simulator supporting both GUI visualization (via Tkinter) and high-throughput headless simulation for benchmarking

Performance-critical components such as legal placement generation and piece drop locations are memoized to avoid redundant computation during search.

## Results
Agents were evaluated using a headless simulation framework across increasing horizons (10–200 pieces per run). While baseline Expectimax performed reasonably in short games, the beamsearchChance  agent consistently cleared more lines on average as game length increased, demonstrating improved long-term decision quality in addition to better scalability.

This beamsearchChance agent was able to run autonomously for extended horizons, achieving 8,000+ lines cleared in long-running simulations and outperforming standard Expectimax in average lines-per-piece across all larger test cases.


### References
Pierre Dellacherie, “The Best Known Algorithms for Playing Tetris” (unpublished heuristic algorithm, widely cited in Tetris AI literature)

M. Bodoia & A. Puranik, Applying Reinforcement Learning to Competitive Tetris, Stanford University

T. Gilliland & D. Zhang, Parallel Greedy Tetris Solver, Columbia University