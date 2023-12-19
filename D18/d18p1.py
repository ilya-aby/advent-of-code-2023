"""
This module solves Part One of Day 18's problem of the Advent of Code challenge.
The approach here is that we build a polygon in a grid and then use raycasting to implement
a point-in-polygon algorithm to determine whether a tile is inside or outside the polygon to
decide if we should fill it. In part 2, we see this doesn't scale very far. Even on this input,
the point-in-poly approach takes 5+ mins to run.
"""
# --- Day 18: Lavaduct Lagoon ---
# Thanks to your efforts, the machine parts factory is one of the first factories up and running
# since the lavafall came back. However, to catch up with the large backlog of parts requests, the
# factory will also need a large supply of lava for a while; the Elves have already started creating
# a large lagoon nearby for this purpose.
#
# However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the
# dig plan (your puzzle input). For example:
#
# R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)
# The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of
# meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The
# directions are given as seen from above, so if "up" were north, then "right" would be east, and so
# on. Each trench is also listed with the color that the edge of the trench should be painted as an
# RGB hexadecimal color code.
#
# When viewed from above, the above example dig plan would result in the following loop of trench
# (#) having been dug out from otherwise ground-level terrain (.):
#
# #######
# #.....#
# ###...#
# ..#...#
# ..#...#
# ###.###
# #...#..
# ##..###
# .#....#
# .######
# At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of
# the lagoon; the next step is to dig out the interior so that it is one meter deep as well:
#
# #######
# #######
# #######
# ..#####
# ..#####
# #######
# #####..
# #######
# .######
# .######
# Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is
# dug out, the edges are also painted according to the color codes in the dig plan.
#
# The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many
# cubic meters of lava could it hold?
#
# Your puzzle answer was 38188

from icecream import ic
from tqdm import tqdm

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    data = open(filename).read().strip()
    lines = data.split('\n')
    data = []
    for row in lines:
        vector, amt, color = row.split(' ')
        data.append([vector, int(amt), color.strip('()')])
    return ic(data)

def dig(data):
    """
    Takes in a list of instructions and returns a grid and a list of edges.
    """
    vector_map = { 'R': (0,1), 'L': (0,-1), 'U': (-1,0), 'D': (1,0) }
    
    min_row = 0
    max_row = 0
    min_col = 0
    max_col = 0
    
    location = (0,0)
    for instruction in data:
        vector, amt, color = instruction
        vector_offset = vector_map[vector]
        for x in range(amt):
            location = (location[0] + vector_offset[0], location[1] + vector_offset[1])
        min_row = min(min_row, location[0])
        max_row = max(max_row, location[0])
        min_col = min(min_col, location[1])
        max_col = max(max_col, location[1])  
    width = max_col - min_col + 1
    height = max_row - min_row + 1  
    ic(min_row, max_row, min_col, max_col, width, height)
    
    # Create an empty array of width x height
    grid = [['.' for x in range(width)] for y in range(height)]
    edges = []
    
    # Offset the location by the minimum row and column
    location = (abs(min_row), abs(min_col))
 
    for instruction in data:
        vector, amt, color = instruction
        vector_offset = vector_map[vector]
        ic(vector, amt, color, vector_offset, location)
        for x in range(amt):
            location = (location[0] + vector_offset[0], location[1] + vector_offset[1])
            #grid[location[0]][location[1]] = color
            edges.append(location)
            grid[location[0]][location[1]] = '#'

    return grid, edges
    
def infill(data, edges):
    """
    Goes through every tile in data. For the blank ('.') tiles, uses point-in-poly raycasting
    to determine whether the tile is inside or outside the polygon. If inside, fills with '#'
    """
    for row in tqdm(range(len(data))):
        for col in range(len(data[0])):
            if data[row][col] == '.':
                if is_inside_polygon(row, col, data, edges):
                    data[row][col] = '+'
                else:
                    data[row][col] = '.'
    return ic(data)

def is_inside_polygon(row, col, grid, edges):
    """ Raycasting point-in-poly algorithm """
    intersections = 0
    x, y = row, col
    grid_height = len(grid) # Number of rows
    grid_width = len(grid[0]) # Number of columns
    
    while x < grid_height and y < grid_width:
        if (x,y) in edges and not is_corner((x,y), grid):
            intersections += 1
        x += 1
        y += 1
    return intersections % 2 == 1

def is_corner(point, grid):
    """
    Checks if a point is a corner in the grid.
    A point is considered a corner if it matches one of two possible adverse corner configurations.
    """
    x, y = point
    max_x = len(grid) - 1
    max_y = len(grid[0]) - 1

    # Check for corner configuration 1
    if x > 0 and y < max_y and grid[x-1][y] == '#' and \
        grid[x][y+1] == '#' and grid[x-1][y+1] == '.':
        return True
    # Check for corner configuration 2
    if x < max_x and y > 0 and grid[x+1][y] == '#' and \
        grid[x][y-1] == '#' and grid[x+1][y-1] == '.':
        return True
    return False

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    instructions = parse_input("sample.txt")
    grid, edges = dig(instructions)
    print(edges)
    ic(grid)
    infill(grid, edges)
    
    count_tiles = 0
    for row in grid:
        for char in row:
            if char == '.':
                print('.', end='')
            else:
                print('#', end='')
                count_tiles += 1
        print()
    print(count_tiles)

if __name__ == "__main__":
    main()
