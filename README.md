# advent-of-code-2023

### Purpose
* My solutions in Python to [Advent of Code](https://adventofcode.com/) 2023
* For this year, focusing on learning Python best-practices & how to pair effectively with LLMs

### Index
* Day 1: [Part 1](/D01/d1p1.py) & [Part 2](/D01/d1p2.py) - Merging digits from the ends of a string
* Day 2: [Part 1](/D02/d2p1.py) & [Part 2](/D02/d2p2.py) - Colored ball game
* Day 3: [Part 1](/D03/d3p1.py) & [Part 2](/D03/d3p2.py) - Engine parts and gears
* Day 4: [Part 1](/D04/d4p1.py) & [Part 2](/D04/d4p2.py) - Scratchcards
* Day 5: [Part 1](/D05/d5p1.py) & [Part 2](/D05/d5p2.py) - Seed Maps
* Day 6: [Part 1](/D06/d6p1.py) & [Part 2](/D06/d6p2.py) - Boat Races
* Day 7: [Part 1](/D07/d7p1.py) & [Part 2](/D07/d7p2.py) - Camel Poker
* Day 8: [Part 1](/D08/d8p1.py) & [Part 2](/D08/d8p2.py) - Camel Maps
* Day 9: [Part 1](/D09/d9p1.py) & [Part 2](/D09/d9p2.py) - Sequence Prediction
* Day 10: [Part 1](/D10/d10p1.py) & [Part 2](/D10/d10p2.py) - Pipe Maze
* Day 11: [Part 1](/D11/d11p1.py) & [Part 2](/D11/d11p2.py) - Galaxy Maps
* Day 12: [Part 1](/D12/d12p1.py) & [Part 2](/D12/d12p2.py) - Broken Springs
* Day 13: [Part 1](/D13/d13p1.py) & [Part 2](/D13/d13p2.py) - Mirrored Lava Map
* Day 14: [Part 1](/D14/d14p1.py) & [Part 2](/D14/d14p2.py) - Rolling Rocks
* Day 15: [Part 1](/D15/d15p1.py) & [Part 2](/D15/d15p2.py) - Lens Library
* Day 16: [Part 1](/D16/d16p1.py) & [Part 2](/D16/d16p2.py) - Light Beams and Mirrors
* Day 17: [Part 1](/D17/d17p1.py) & [Part 2](/D17/d17p2.py) - Sliding Crucible
* Day 18: [Part 1](/D18/d18p1.py) & [Part 2](/D18/d18p2.py) - Digging Trenches
* Day 19: [Part 1](/D19/d19p1.py) & [Part 2](/D19/d19p2.py) - Instruction Intervals
* Day 20: [Part 1](/D20/d20p1.py) & [Part 2](/D20/d20p2.py) - Modules
* Day 21: [Part 1](/D21/d21p1.py) & [Part 2](/D21/d21p2.py) - Garden Step Counter
* Day 22: [Part 1](/D22/d22p1.py) & [Part 2](/D22/d22p2.py) - Falling Sand Slabs
* Day 23: [Part 1](/D23/d23p1.py) & [Part 2](/D23/d23p2.py) - Longest Walk
* Day 24: [Part 1](/D24/d24p1.py) & [Part 2](/D24/d24p2.py) - Colliding Hailstones
* Day 25: [Part 1](/D25/d25p1.py) - Cutting Wires

### Lessons Learned This Year
**Python Basics:**
* Using `file.read().splitlines()` and `split()` to efficiently ingest delineated input data
* Using Python string methods like `.find()` and `.replace()` instead of regulare expressions
* Using docstrings at the top of modules and function definitions
* Iterating over dictionaries and lists with `enumerate()` and `items()` instead of i = 1 to length
* Using `all()` and `any()` to test contents of iterable objects
* Using the debugger and conditional breakpoints to step into the program at specific times

**Python Libraries:**
* Using `tqdm` to estimate progress time for long-running scripts
* Using `icecream` to debug outputs
* Using `networkx` for manipulating graphs
* Using `@cache` decorator from `functools` to automatically memoize a function
* Using `graphviz` to visualize network graphs 
* Using `matplotlib` to create 3D visualizations of lines & polygons for problems in 3D space
* Using `sympy` to solve systems of equations 

**General Algorithms & Data Structures:**
* Using stacks in place of recursion and running DFS/BFS with a `while queue` loop
* Sub-note: swapping between DFS nand BFS is often as easy as changing .pop() to .pop(0)
* Using Dijkstra's for finding minimum cost paths through graphs with unequal weights
* Ray casting from a point to determine if it's inside or outside a polygon
* Using Shoelace Theorem and Pick's Theorem to calculate area of a polygon

**AoC-specific Tricks:**
* Inspecting the input for hidden properties not mentioned in the problem
* Logging x --> f(x) values to manually find cycles and patterns
* Visually inspecting network graphs and grids for unusual patterns or bottlenecks
* Using pre-made templates to speed up getting started on a new problem

**IDE / VSCode**
* Using `Pylint`, `Error Lens`, and `autopep8` to format code