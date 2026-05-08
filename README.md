Maze Generator and Solver (DFS Backtracking)

Project Overview
This project is a Python-based maze generator and solver built using Pygame. It generates a perfect random maze using Depth First Search (DFS) with backtracking and then solves it using a pathfinding algorithm with visual animation.

The goal is to simulate an “exploring mouse” that carves a maze and later finds its way from start to finish.

Features
- Random maze generation using DFS (stack-based backtracking)
- Guaranteed fully connected maze (perfect maze)
- Visual rendering using Pygame
- Maze solver with animated traversal
- Dead-end detection and visualization
- Bonus: Random wall breaking (creates cycles)

Algorithm Explanation

### Maze Generation
- Start with a full grid where all walls are intact
- Use Depth First Search (DFS) with a stack
- From the current cell:
  - Randomly choose an unvisited neighbor
  - Remove the wall between cells
  - Push current cell to stack
  - Move to next cell
- If no neighbors exist, backtrack using the stack
- Repeat until all cells are visited

This guarantees a “perfect maze” (no disconnected sections).

Maze Representation
The maze is represented using:
- northWall[i][j] → top wall of each cell
- eastWall[i][j] → right wall of each cell

Left and bottom walls are inferred from adjacent cells.

Maze Solver
- Starts at entrance cell
- Moves through open paths
- Uses backtracking with a stack
- Marks:
  - 🔴 Red = current position
  - 🔵 Blue = dead ends
  - 🟩 Green = successful path

Bonus Feature
To make the maze more interesting, there is a 1 in 20 chance that a wall is removed randomly during generation. This creates loops and breaks the “perfect maze” structure, making solving more complex.

 How to Run
```bash
python main.py