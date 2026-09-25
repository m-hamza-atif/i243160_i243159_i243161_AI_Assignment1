# ARTIFICIAL INTELLIGENCE (A12002) - ASSIGNMENT 01
```
By:-
Muhammad Hamza Atif     (24I-3160)
Muhammad Saim Hassan    (24I-3159)
Muhammad Hassan         (24I-3161)
```

## PYTHON & SYSTEM REQUIREMENTS:
- Python Version: Python 3.8+ (Tested on Python 3.12)
- Operating System: Linux / macOS / Windows 11
- Libraries Used: util, sys, os, csv, heapq

## EXECUTION COMMANDS:
To run full autograder suite: `python autograder.py`

To run specific algorithm questions:
```
  python autograder.py -q q1   # DFS
  python autograder.py -q q2   # BFS
  python autograder.py -q q3   # UCS
  python autograder.py -q q4   # A*
  python autograder.py -q q5   # Corners Problem
  python autograder.py -q q6   # Corners Heuristic
  python autograder.py -q q7   # Food Search Heuristic
  python autograder.py -q q8   # Closest Dot Search
```

To run manual maze tests:
```
  python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
  python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
  python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
  python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
  python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```