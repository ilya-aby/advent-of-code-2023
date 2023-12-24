"""
This module solves Part One of Day 23's problem of the Advent of Code challenge.
Approach here is just a simple DFS through the maze, keeping track of the longest path found so far.
We handle "slides" by adding the slide position and post-slide position to the path and visited set.

Lots of time lost here debugging that all the DFS paths were sharing one visited set when they
actually each needed their own copy.
"""

# --- Day 23: A Long Walk ---
# The Elves resume water filtering operations! Clean water starts flowing over the edge of Island
# Island.
#
# They offer to help you go over the edge of Island Island, too! Just hold on tight to one end of
# this impossibly long rope and they'll lower you down a safe distance from the massive waterfall
# you just created.
#
# As you finally reach Snow Island, you see that the water isn't really reaching the ground: it's
# being absorbed by the air itself. It looks like you'll finally have a little downtime while the
# moisture builds up to snow-producing levels. Snow Island is pretty scenic, even without any snow;
# why not take a walk?
#
# There's a map of nearby hiking trails (your puzzle input) that indicates paths (.), forest (#),
# and steep slopes (^, >, v, and <).
#
# For example:
#
# #.#####################
# #.......#########...###
# #######.#########.#.###
# ###.....#.>.>.###.#.###
# ###v#####.#v#.###.#.###
# ###.>...#.#.#.....#...#
# ###v###.#.#.#########.#
# ###...#.#.#.......#...#
# #####.#.#.#######.#.###
# #.....#.#.#.......#...#
# #.#####.#.#.#########v#
# #.#...#...#...###...>.#
# #.#.#v#######v###.###v#
# #...#.>.#...>.>.#.###.#
# #####v#.#.###v#.#.###.#
# #.....#...#...#.#.#...#
# #.#########.###.#.#.###
# #...###...#...#...#.###
# ###.###.#.###v#####v###
# #...#...#.#.>.>.#.>.###
# #.###.###.#.###.#.#v###
# #.....###...###...#...#
# #####################.#
# You're currently on the single path tile in the top row; your goal is to reach the single path
# tile in the bottom row. Because of all the mist from the waterfall, the slopes are probably quite
# icy; if you step onto a slope tile, your next step must be downhill (in the direction the arrow is
# pointing). To make sure you have the most scenic hike possible, never step onto the same tile
# twice. What is the longest hike you can take?
#
# In the example above, the longest hike you can take is marked with O, and your starting position
# is marked S:
#
# #S#####################
# #OOOOOOO#########...###
# #######O#########.#.###
# ###OOOOO#OOO>.###.#.###
# ###O#####O#O#.###.#.###
# ###OOOOO#O#O#.....#...#
# ###v###O#O#O#########.#
# ###...#O#O#OOOOOOO#...#
# #####.#O#O#######O#.###
# #.....#O#O#OOOOOOO#...#
# #.#####O#O#O#########v#
# #.#...#OOO#OOO###OOOOO#
# #.#.#v#######O###O###O#
# #...#.>.#...>OOO#O###O#
# #####v#.#.###v#O#O###O#
# #.....#...#...#O#O#OOO#
# #.#########.###O#O#O###
# #...###...#...#OOO#O###
# ###.###.#.###v#####O###
# #...#...#.#.>.>.#.>O###
# #.###.###.#.###.#.#O###
# #.....###...###...#OOO#
# #####################O#
# This hike contains 94 steps. (The other possible hikes you could have taken were 90, 86, 82, 82,
# and 74 steps long.)
#
# Find the longest hike you can take through the hiking trails listed on your map. How many steps
# long is the longest hike?
#
# Your puzzle answer was 2414.
#

import time
from icecream import ic

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    
    with open(filename, 'r') as file:
        maze = file.read().splitlines()
    
    return maze

def walk_maze(maze):
    """
    Does a DFS through the maze, keeping track of the longest path found so far
    """
    start = (0, 1)
    end = (len(maze) - 1, len(maze[0]) - 2)
    paths = [([start], set([start]))]  # Each path now also keeps track of its own visited set
    slide_vectors = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
    
    longest_path = []
    
    while paths:
        # Get the last path in the list
        path, visited = paths.pop()
        cur_row, cur_col = path[-1]
            
        # If this path is longer than the current longest path, update longest_path
        if len(path) > len(longest_path) and (cur_row, cur_col) == end:
            longest_path = path
        
        for next_row, next_col in [(cur_row+1, cur_col), (cur_row-1, cur_col), 
                                   (cur_row, cur_col+1), (cur_row, cur_col-1)]:
            # Bounds checking to make sure we stay within maze
            if next_row < 0 or next_row >= len(maze) or next_col < 0 or next_col >= len(maze[0]):
                continue
            if maze[next_row][next_col] == '#':
                continue
            if (next_row, next_col) in visited:
                continue
            if maze[next_row][next_col] in ['>', '<', '^', 'v']:
                # Continue in the direction of the slide
                slide_vector = slide_vectors[maze[next_row][next_col]]
                slide_row = next_row + slide_vector[0]
                slide_col = next_col + slide_vector[1]

                # Add the slide position and post-slide position to the path and visited set 
                # if they haven't been visited
                if (slide_row, slide_col) not in visited:
                    visited.add((slide_row, slide_col))
                    new_path = path + [(next_row, next_col), (slide_row, slide_col)] 
                    paths.append((new_path, visited.copy()))
            else:
                # Just a regular step, can add it to visited & path
                visited.add((next_row, next_col))
                paths.append((path + [(next_row, next_col)], visited.copy()))    
    
    # Subtract 1 because starting square is not counted
    return len(longest_path) - 1

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

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    data = parse_input("input.txt")
    
    start_time = time.time()
    longest_path = walk_maze(data)
    elapsed_time = time.time() - start_time
    
    print(f"Longest path: {longest_path}. Time elapsed: {round(elapsed_time, 2)} seconds.")

if __name__ == "__main__":
    main()
