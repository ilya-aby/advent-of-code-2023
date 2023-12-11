"""
This module solves Part Two of Day 10's problem of the Advent of Code challenge.
This was extremely challenging. This particular solution uses ray-casting to implement
a point-in-polygon algorithm. We cast a ray out from each tile and count intersecting polygon
segments. If the number is odd, the tile is inside the polygon. If the number is even, the tile
is outside. Hard edge cast here is that we cast diagonally to avoid colinear segments and we
have to skip corner tiles to avoid tangential intersections.


Other possible approaches here would be to flood fill the maze and count the number of enclosed
tiles, but that would require a lot of extra work to handle flooding "in between" unconnected
pipe segments, possibly by expanding the maze. We also maybe could have tried traversing the
pipe edge and marking "left" and "right" tiles as we go, then flood filling until we hit left
or right and then filling any other junk tiles that were touched on that side.
"""
# --- Part Two ---
# You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is
# within the area enclosed by the loop?
#
# To determine whether it's even worth taking the time to search for such a nest, you should
# calculate how many tiles are contained within the loop. For example:
#
# ...........
# .S-------7.
# .|F-----7|.
# .||.....||.
# .||.....||.
# .|L-7.F-J|.
# .|..|.|..|.
# .L--J.L--J.
# ...........
# The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast
# (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop
# again with those regions marked:
#
# ...........
# .S-------7.
# .|F-----7|.
# .||OOOOO||.
# .||OOOOO||.
# .|L-7OF-J|.
# .|II|O|II|.
# .L--JOL--J.
# .....O.....
# In fact, there doesn't even need to be a full tile path to the outside for tiles to count as
# outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O
# is still outside the loop:
#
# ..........
# .S------7.
# .|F----7|.
# .||OOOO||.
# .||OOOO||.
# .|L-7F-J|.
# .|II||II|.
# .L--JL--J.
# ..........
# In both of the above examples, 4 tiles are enclosed by the loop.
#
# Here's a larger example:
#
# .F----7F7F7F7F-7....
# .|F--7||||||||FJ....
# .||.FJ||||||||L7....
# FJL7L7LJLJ||LJ.L-7..
# L--J.L7...LJS7F-7L7.
# ....F-J..F7FJ|L7L7L7
# ....L7.F7||L7|.L7L7|
# .....|FJLJ|FJ|F7|.LJ
# ....FJL-7.||.||||...
# ....L---J.LJ.LJLJ...
# The above sketch has many random bits of ground, some of which are in the loop (I) and some of
# which are outside it (O):
#
# OF----7F7F7F7F-7OOOO
# O|F--7||||||||FJOOOO
# O||OFJ||||||||L7OOOO
# FJL7L7LJLJ||LJIL-7OO
# L--JOL7IIILJS7F-7L7O
# OOOOF-JIIF7FJ|L7L7L7
# OOOOL7IF7||L7|IL7L7|
# OOOOO|FJLJ|FJ|F7|OLJ
# OOOOFJL-7O||O||||OOO
# OOOOL---JOLJOLJLJOOO
# In this larger example, 8 tiles are enclosed by the loop.
#
# Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another
# example with many bits of junk pipe lying around that aren't connected to the main loop at all:
#
# FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L
# Here are just the tiles that are enclosed by the loop marked with I:

# FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJIF7FJ-
# L---JF-JLJIIIIFJLJJ7
# |F|F-JF---7IIIL7L|7|
# |FFJF7L7F-JF7IIL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L
# In this last example, 10 tiles are enclosed by the loop.
#
# Figure out whether you have time to search for the nest by calculating the area within the loop.
# How many tiles are enclosed by the loop?
# 
# 
# Answer for input: 529

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


def get_next_step(maze: list[list[str]], current_coords: tuple[int, int], current_symbol: str, prev_coords: tuple[int,int]) -> tuple[int, int]:
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
        
    # If we're not at the animal, check the symbol and go away from where we came from along the pipe
    # Start by getting the vector from the previous coords to the current coords
    # Then look up the symbol's possible exits and take the one that's not the one we came from
    prev_vs_cur = (prev_coords[0] - current_coords[0], prev_coords[1] - current_coords[1])
    if symbol_directions[current_symbol][0] == prev_vs_cur:
        return (current_coords[0] + symbol_directions[current_symbol][1][0], current_coords[1] + symbol_directions[current_symbol][1][1])
    else:
        return (current_coords[0] + symbol_directions[current_symbol][0][0], current_coords[1] + symbol_directions[current_symbol][0][1])

def get_pipe_coordinates(maze: list[list[str]]) -> list[tuple[int, int]]:
    """
    Finds the animal, then traverses maze until it cycles back to start
    Keeps track of coordinates of all valid pipe segments
    """
    # Find animal
    animal_coords = None
    for row_index, row in enumerate(maze):
        if 'S' in row:
            animal_coords = (row_index, row.index('S'))

    # Traverse maze starting from the animal
    steps_taken = 0
    current_coords = animal_coords
    current_symbol = 'S'
    prev_coords = None
    pipe_coords = []

    # Check around animal for a valid path leading away from it
    while(True):
        next_coords = get_next_step(maze, current_coords, current_symbol, prev_coords)
        if next_coords is None:
            print(f'ERROR: No valid path found for {current_symbol} at {current_coords}')
            return 0
        steps_taken += 1
        prev_coords = current_coords
        current_coords = next_coords
        pipe_coords.append(current_coords)
        current_symbol = maze[current_coords[0]][current_coords[1]]

        # If we've looped back to the animal, we're done
        if current_symbol == 'S':
            return pipe_coords

def flood_fill(maze: list[list[str]], pipe_coordinates: list[tuple[int, int]], coords_to_visit: tuple[int, int]):
    """
    Flood fills the maze to find the enclosed tiles
    """

    print(f'Flood filling {coords_to_visit}')
    for line in maze:
        print(''.join(line))
    print("\n")

    # Check if tile is out of bounds
    if coords_to_visit[0] < 0 or coords_to_visit[0] >= len(maze) or coords_to_visit[1] < 0 or coords_to_visit[1] >= len(maze[0]):
        return

    # Check if tile is a pipe segment
    if coords_to_visit in pipe_coordinates:
        return
    
    # Check if tile has already been flooded
    if maze[coords_to_visit[0]][coords_to_visit[1]] == 'O':
        return
    
    # Mark tile as flooded
    maze[coords_to_visit[0]][coords_to_visit[1]] = 'O'

    for line in maze:
        print(''.join(line))
    print("\n")
    
    # Recursively flood fill the tile and those around it
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:  # Avoid adding the current tile
                flood_fill(maze, pipe_coordinates, (coords_to_visit[0] + dx, coords_to_visit[1] + dy))

def is_point_in_poly(maze: list[list[str]], pipe_coordinates: list[tuple[int, int]], point: tuple[int, int]) -> bool:
    """
    Ray casts from a point diagonally to the right to see if it intersects with the polygon
    """
    x, y = point
    intersections = 0
    maze_height = len(maze)
    maze_width = len(maze[0])

    # Cast the ray diagonally to the right
    while x < maze_width and y < maze_height:
        if (x, y) in pipe_coordinates and maze[x][y] not in ['L', '7']:
            intersections += 1
        x += 1
        y += 1

    #print(f'Casting ray from {point} diagonally to the right, found {intersections} intersections')

    # If the number of intersections is odd, the point is inside the polygon
    return intersections % 2 == 1
    


def count_enclosed(maze: list[list[str]], pipe_coordinates: list[tuple[int, int]]) -> int:
    """
    Counts all tiles that are not marked as 'O' and are not pipe segments
    """
    enclosed_tiles = 0
    for row_index, row in enumerate(maze):
        for col_index, col in enumerate(row):
            if col != 'O' and (row_index, col_index) not in pipe_coordinates:
                enclosed_tiles += 1
                maze[row_index][col_index] = 'I'
    return enclosed_tiles

def main():
    """
    Main function that reads the input file, parses the maze, and finds farthest point
    """
    maze = parse_maze(FILENAME)
    pipe_coordinates = get_pipe_coordinates(maze)

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i,j) in pipe_coordinates:
                continue
            if is_point_in_poly(maze, pipe_coordinates, (i, j)):
                maze[i][j] = 'I'
            else:
                maze[i][j] = 'O'

    for line in maze:
        print(''.join(line))

    # Count the number of enclosed tiles, which will be any remaining characters that aren't flooded and aren't pipes
    print(f'Number of enclosed tiles: {count_enclosed(maze, pipe_coordinates)}')


    #print(f'Number of enclosed tiles: {count_enclosed_tiles(maze, pipe_coordinates)}')
     
if __name__ == "__main__":
    main()
