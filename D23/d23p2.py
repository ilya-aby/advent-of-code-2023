"""
This module solves Part Two of Day 23's problem of the Advent of Code challenge.

This is a 'longest path' problem and is NP hard, but inspecting the input shows us that there
are very few junctions and a lot of long, narrow hallways. We "compress" the maze into a graph
where the edge weights between nodes are the lengths of those hallways. Then we can use DFS to
find the longest path much faster. This still takes about 17 seconds, but without the compression
would run endlessly.
"""

# --- Part Two ---
# As you reach the trailhead, you realize that the ground isn't as slippery as you expected; you'll
# have no problem climbing up the steep slopes.
#
# Now, treat all slopes as if they were normal paths (.). You still want to make sure you have the
# most scenic hike possible, so continue to ensure that you never step onto the same tile twice.
# What is the longest hike you can take?
#
# In the example above, this increases the longest hike to 154 steps:
#
# #S#####################
# #OOOOOOO#########OOO###
# #######O#########O#O###
# ###OOOOO#.>OOO###O#O###
# ###O#####.#O#O###O#O###
# ###O>...#.#O#OOOOO#OOO#
# ###O###.#.#O#########O#
# ###OOO#.#.#OOOOOOO#OOO#
# #####O#.#.#######O#O###
# #OOOOO#.#.#OOOOOOO#OOO#
# #O#####.#.#O#########O#
# #O#OOO#...#OOO###...>O#
# #O#O#O#######O###.###O#
# #OOO#O>.#...>O>.#.###O#
# #####O#.#.###O#.#.###O#
# #OOOOO#...#OOO#.#.#OOO#
# #O#########O###.#.#O###
# #OOO###OOO#OOO#...#O###
# ###O###O#O###O#####O###
# #OOO#OOO#O#OOO>.#.>O###
# #O###O###O#O###.#.#O###
# #OOOOO###OOO###...#OOO#
# #####################O#
# Find the longest hike you can take through the surprisingly dry hiking trails listed on your map.
# How many steps long is the longest hike?
#
# Your puzzle answer was 6598.

import time
from icecream import ic

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    
    with open(filename, 'r') as file:
        maze = file.read().splitlines()
        
    # Replace every '>', "<", "^", "v" with a . character
    for row in range(len(maze)):
        maze[row] = maze[row].replace('>', '.')
        maze[row] = maze[row].replace('<', '.')
        maze[row] = maze[row].replace('^', '.')
        maze[row] = maze[row].replace('v', '.')
    
    return maze

def animate_maze(maze, path):
    """
    Helper function to show the path through the maze
    """
    
    # Create a copy of the maze to modify
    maze_copy = [list(row) for row in maze]
    
    # Mark the start and end points
    maze_copy[0][1] = 'S'
    maze_copy[-1][-2] = 'E'
    
    # Mark the path
    for row, col in path:
        maze_copy[row][col] = 'X'
        # Print the maze
    for row in maze_copy:
        print(''.join(row))
    input()
    
    return

def convert_to_graph(maze):
    """
    Reads in the maze and compresses it into a graph representation
    The maze has few junctions and a lot of long hallways, so we can compress it by
    representing each hallway as a single node and each junction as a node. The nodes are
    connected by edges with weights equal to the length of the hallway. That way, we can
    use DFS to find the longest path much faster.
    """
    start = (0, 1)
    end = (len(maze) - 1, len(maze[0]) - 2)
    
    # Find critical nodes defined as start, end, or junctions
    nodes = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '#':
                continue
            neighbors = 0
            for neighbor in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
                if in_bounds_and_not_a_wall(neighbor, maze):
                    neighbors += 1               
            if neighbors != 2 or (i, j) in [start, end]:  # Not a corridor or start/end
                nodes.append((i, j))
    
    # Go through each node and run a DFS to branch out and find the other nodes, then update
    # edge weights to be the length of the hallway connecting the nodes
    graph = {node: [] for node in nodes}
    for node in nodes:
        stack = [(node, 0)]  # Stack for DFS, each element is a tuple (current position, cost)
        visited = set()
        while stack:
            current, cost = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            if current in nodes and current != node:
                graph[node].append((current, cost))
                continue
            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x, y = current[0] + direction[0], current[1] + direction[1]
                if in_bounds_and_not_a_wall((x, y), maze):
                    stack.append(((x, y), cost + 1))
    
    return graph

def dfs_graph(graph):
    """
    Does a DFS on a graph representation of a maze to find the longest path
    This problem is NP-hard, so we the only reason this works is because the maze is
    very narrow and has few junctions & we can compress it into a graph representation.
    """

    start = (0, 1)
    end = (140, 139)
    stack = [(start, 0, [], set())]  # Stack for DFS: (current node, cost, path, visited)
    max_cost = 0

    while stack:
        current, cost, path, visited = stack.pop()

        if current == end and cost > max_cost:
            max_cost = cost

        if current in visited:
            continue

        visited.add(current)
        path = path + [current]

        for neighbor, weight in graph[current]:
            if neighbor not in visited:  # Avoid cycles
                stack.append((neighbor, cost + weight, path, visited.copy()))

    return max_cost

def in_bounds_and_not_a_wall(coordinates, maze):
    """
    Helper function to check if a position is within the maze
    """
    row = coordinates[0]
    col = coordinates[1]
    return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] != '#'

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    maze = parse_input("input.txt")
    start_time = time.time()
    graph = convert_to_graph(maze)
    max_cost = dfs_graph(graph)
    elapsed_time = time.time() - start_time
    print(f"Longest path: {max_cost}. Time elapsed: {round(elapsed_time, 2)} seconds.")

if __name__ == "__main__":
    main()
