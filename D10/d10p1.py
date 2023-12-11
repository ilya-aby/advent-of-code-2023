"""
This module solves Part One of Day 10's problem of the Advent of Code challenge.
Approach is just to store movement vectors for the possible maze symbols
We find the animal tile then traverse the full length of the pipe loop and cut that
in half to the get the maximum distance.
"""
# --- Day 10: Pipe Maze --- You use the hang glider to ride the hot air from Desert Island all the
# way up to the floating metal island. This island is surprisingly cold and there definitely aren't
# any thermals to glide on, so you leave your hang glider behind.
#
# You wander around for a while, but you don't find any people or animals. However, you do
# occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction;
# maybe you can find someone at the hot springs and ask them where the desert-machine parts are
# made.
#
# The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire
# some metal grass, you notice something metallic scurry away in your peripheral vision and jump
# into a big pipe! It didn't look like any animal you've ever seen; if you want a better look,
# you'll need to get ahead of it.
#
# Scanning the area, you discover that the entire field you're standing on is densely packed with
# pipes; it was hard to tell at first because they're the same metallic silver color as the
# "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).
#
# The pipes are arranged in a two-dimensional grid of tiles:
#
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west. L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west. 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east. . is ground; there is no pipe in this tile. S is
# the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show
# what shape the pipe has. Based on the acoustics of the animal's scurrying, you're confident the
# pipe that contains the animal is one large, continuous loop.
#
# For example, here is a square loop of pipe:
#
# ..... .F-7. .|.|. .L-J. ..... If the animal had entered this loop in the northwest corner, the
# sketch would instead look like this:
#
# ..... .S-7. .|.|. .L-J. ..... In the above diagram, the S tile is still a 90-degree F bend: you
# can tell because of how the adjacent pipes connect to it.
#
# Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the
# same loop as above:
#
# -L|F7
# 7S-7| L|7|| -L-J| L|-JF In the above diagram, you can still figure out which pipes form the main
# loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to,
# and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have
# exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).
#
# Here is a sketch that contains a slightly more complex main loop:
#
# ..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ...
# Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:
#
# 7-F7-
# .FJ|7
# SJLL7
# |F--J
# LJ.LJ
#
# If you want to get out ahead of the animal, you should find the tile in the loop that is farthest
# from the starting position. Because the animal is in the pipe, it doesn't make sense to measure
# this by direct distance. Instead, you need to find the tile that would take the longest number of
# steps along the loop to reach from the starting point - regardless of which way around the loop
# the animal went.
#
# In the first example with the square loop:
#
# .....
# .S-7.
# .|.|.
# .L-J.
# .....
# You can count the distance each tile in the loop is from the starting point like this:
#
# .....
# .012.
# .1.3.
# .234.
# .....
# In this example, the farthest point from the start is 4 steps away.
#
# Here's the more complex loop again:
#
# ..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ...
# Here are the distances for each tile on that loop:
#
# ..45.
# .236.
# 01.78
# 14567
# 23...
# 
# Find the single giant loop starting at S. How many steps along the loop does it take to get from
# the starting position to the point farthest from the starting position?
# 
# Answer for sample input: 4
# Answer for input: 6923

FILENAME = 'input.txt'

def parse_maze(file_name: str) -> list[list[str]]:
    """
    Parses a maze file and returns a list of lists containing the maze characters
    """

    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e
    
    maze = [list(line.strip()) for line in data]

    return maze


def get_next_step(maze: list[list[str]], 
                  current_coords: tuple[int, int], 
                  current_symbol: str, 
                  prev_coords: tuple[int,int]) -> tuple[int, int]:
    """
    Returns the coordinates of the next step in the maze
    """

    # Defines how the symbols map to directions
    symbol_directions = {'-': [(0, -1), (0, 1)],
                        '|': [(-1, 0), (1, 0)],
                        'L': [(-1, 0), (0, 1)],
                        '7': [(0, -1), (1, 0)],
                        'J': [(0, -1), (-1, 0)],
                        'F': [(1, 0), (0, 1)]}

    # Special case: If we're at the animal, we can go anywhere valid
    if current_symbol == 'S':
        # Check above
        if current_coords[0] > 0 and maze[current_coords[0] - 1][current_coords[1]] in ['F','|','7']:
            return (current_coords[0] - 1, current_coords[1])
        # Check below
        if current_coords[0] < len(maze) - 1 and maze[current_coords[0] + 1][current_coords[1]] in ['J','|','L']:
            return (current_coords[0] + 1, current_coords[1])
        # Check left
        if current_coords[1] > 0 and maze[current_coords[0]][current_coords[1] - 1] in ['L','-','F']:
            return (current_coords[0], current_coords[1] - 1)
        # Check right
        if current_coords[1] < len(maze[0]) - 1 and maze[current_coords[0]][current_coords[1] + 1] in ['7','-','J']:
            return (current_coords[0], current_coords[1] + 1)
        else:
            return None
        
    # If we're not at the animal, check the symbol and go away from where we came from along the
    # pipe. Start by getting the vector from the previous coords to the current coords. Then look up
    # the symbol's possible exits and take the one that's not the one we came from
    prev_vs_cur = (prev_coords[0] - current_coords[0], prev_coords[1] - current_coords[1])
    if symbol_directions[current_symbol][0] == prev_vs_cur:
        return (current_coords[0] + symbol_directions[current_symbol][1][0], 
                current_coords[1] + symbol_directions[current_symbol][1][1])
        
    return (current_coords[0] + symbol_directions[current_symbol][0][0], 
                current_coords[1] + symbol_directions[current_symbol][0][1])

def get_farthest_point(maze: list[list[str]]) -> int:
    """
    Finds the animal, then traverses maze until it cycles back to start
    Answer will be half the cycle length
    """
    # Find animal
    animal_coords = None
    for row_index, row in enumerate(maze):
        print(row_index, row)
        if 'S' in row:
            animal_coords = (row_index, row.index('S'))
    print(animal_coords)

    # Traverse maze starting from the animal
    steps_taken = 0
    current_coords = animal_coords
    current_symbol = 'S'
    prev_coords = None

    # Check around animal for a valid path leading away from it
    while True:
        next_coords = get_next_step(maze, current_coords, current_symbol, prev_coords)
        if next_coords is None:
            print(f'ERROR: No valid path found for {current_symbol} at {current_coords}')
            return 0
        steps_taken += 1
        prev_coords = current_coords
        current_coords = next_coords
        current_symbol = maze[current_coords[0]][current_coords[1]]

        # If we've looped back to the animal, we're done
        if current_symbol == 'S':
            return steps_taken / 2

def main():
    """
    Main function that reads the input file, parses the maze, and finds farthest point
    """
    maze = parse_maze(FILENAME)
    print(f'Steps to get to farthest point away: {get_farthest_point(maze)}')  
     
if __name__ == "__main__":
    main()
