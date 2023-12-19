"""
This module solves Part One of Day 18's problem of the Advent of Code challenge.
The approach here is that we build a polygon in a grid and then use raycasting to implement
a point-in-polygon algorithm to determine whether a tile is inside or outside the polygon to
decide if we should fill it. In part 2, we see this doesn't scale very far. Even on this input,
the point-in-poly approach takes 5+ mins to run.
"""

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
